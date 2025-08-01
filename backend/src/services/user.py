from typing import Union, Optional, Any
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction
from src.utils.password import pw_manager
from src.utils.jwt import jwt_manager
from src.utils.oauth2 import oauth2
from src.utils.client import JSONClient, http_session
from src.schemas.user import UserBody, LoginUserBody, UpdateUserBody
from src.enums.user import RoleEnum, TokenEnum
from src.clients import Oauth2Client


class UserService(Service):
    def __init__(
        self,
        session: AsyncSession,
        oauth2_client: JSONClient,
        user_repo: Repository,
        telegram_user_repo: Repository
    ):
        super().__init__(session)
        self.repo = user_repo
        self.user_repo = user_repo
        self.telegram_user_repo = telegram_user_repo
        self.jwt = jwt_manager
        self.pw = pw_manager
        self.oauth_manager = oauth2
        self.client = oauth2_client
    
    @transaction
    async def create_one(self, data: UserBody) -> Union[dict, tuple[int, str]]:
        user = await self.user_repo(self.session).get_one_by_username(data.get('username'))
        if user:
            return (422, "Username has already found")
        user = await self.user_repo(self.session).get_one_by_email(data.get("email"))
        if user:
            return (422, "Email has already found")
        password = self.pw.hash_password(data.get('password'))
        data["password"] = password
        return await super().create_one(data)
    
    @transaction
    async def update_one(self, id: Union[int, uuid.UUID], data: UpdateUserBody) -> Union[dict, tuple[int, str]]:
        final_data = dict()
        for key, value in data.items():
            if key != "password" and key != "email" and value is not None:
                user = await self.user_repo(self.session).get_one(**{key: value})
                if user:
                    return (422, f"{key} has already found")
                final_data[key] = value
        pw = data.get("password")
        if pw is not None:
            password = self.pw.hash_password(pw)
            final_data["password"] = password
        phone_number = data.get("phoneNumber")
        if phone_number is not None:
            await self.telegram_user_repo(self.session).update_one_by_phone_number(phone_number, userId=id)
        return await super().update_one(id, final_data)
    
    @transaction
    async def delete_one(self, id: Union[int, uuid.UUID]) -> Union[dict, tuple[int, str]]:
        data = await super().delete_one(id)
        if isinstance(data, tuple):
            return data
        # phone_number = data.get("phoneNumber")
        # if phone_number is not None:
        #     telegram_user = await self.telegram_user_repo(self.session).get_one_by_phone_number(phone_number)
        #     if telegram_user: 
        #         await self.telegram_user_repo(self.session).update_one(telegram_user.id, userId=None)
        return data
    
    async def issue_refresh_token(self, id: int, role: RoleEnum, exp: Optional[int] = None) -> str:
        token = self.jwt.create_refresh_token(str(id), role, exp)
        return token
    
    async def issue_access_token(self, id: int, role: RoleEnum) -> str:
        token = self.jwt.create_access_token(str(id), role)
        return token
    
    async def google_url(self) -> str:
        redirect_uri = self.oauth_manager.google_url_redirect()
        return redirect_uri
    
    @http_session
    @transaction
    async def google_callback(self, code: str) -> Union[dict, tuple[int, str]]:
        oauth2_data = await self.client.get_google_data(code)
        if not oauth2_data:
            return (422, "Invalid google code has sent")
        id_token = oauth2_data.get("id_token")
        oauth2_user_data = self.jwt.decode_oauth2_token(id_token)
        email = oauth2_user_data.get("email")
        user = await self.user_repo(self.session).get_one_by_email(email)
        if not user:
            user_data = dict()
            user_data["email"] = email
            user_data["username"] = email.split("@")[0] + "@"
            user = await super().create_one(user_data)
        else:
            user = user.to_dict()
        refresh_token = await self.issue_refresh_token(user.get("id"), user.get("role"))
        data = dict()
        token_id = str(uuid.uuid4())
        data["user"] = user
        data["tokenId"] = token_id
        await self.redis_manager.set_string_data(f"{token_id}", refresh_token, TokenEnum.REFRESH_TOKEN_EXP.value)
        return data
    
    async def login_user(self, data: LoginUserBody) -> Union[dict, tuple[int, str]]:
        user = await self.user_repo(self.session).get_one_by_username(data.get("username"))
        if not user:
            return (422, "Username has not found")
        user = await self.user_repo(self.session).get_one_by_email(data.get("email"))
        if not user:
            return (422, "Email has not found")
        if isinstance(user, tuple):
            return user
        if not user.password:
            return (422, "User was authenticated via oauth 2.0")
        is_correct_pw = self.pw.check_password(data.get("password"), user.password)
        if not is_correct_pw:
            return (422, "Incorrect password")
        refresh_token = await self.issue_refresh_token(user.id, user.role)
        data = dict()
        token_id = str(uuid.uuid4())
        data["user"] = user
        data["tokenId"] = token_id
        # await self.redis_manager.set_string_data(f"{token_id}:{user.id}", refresh_token, TokenEnum.REFRESH_TOKEN_EXP.value)
        await self.redis_manager.set_string_data(f"{token_id}", refresh_token, TokenEnum.REFRESH_TOKEN_EXP.value)
        return data
    
    async def logout_user(self, token_id: str) -> Union[dict, tuple[int, str]]:
        token = await self.redis_manager.get_string_data(token_id)
        if not token:
            return (400, "Token id or user id has not found")
        payload = self.jwt.validate_token(token)
        if not payload:
            return (400, "User is not authenticated. Refresh token has not found")
        user = await self.user_repo(self.session).get_one_by_id(payload.get("sub"))
        await self.redis_manager.delete(token_id)
        return user.to_dict() if user else None
    
    async def refresh_user(
        self, 
        token_id: Union[str, uuid.UUID]) -> Union[str, tuple[int, str]]:
        # full_id = f"{token_id}:{user_id}"
        token = await self.redis_manager.get_string_data(token_id)
        if not token:
            return (400, "Token id or user id has not found")
        payload = self.jwt.validate_token(token)
        if not payload:
            return (400, "User is not authenticated. Refresh token has not found")
        user = await self.user_repo(self.session).get_one_by_id(int(payload.get("sub")))
        if not user:
            return (400, "Token id or user id has not found")
        new_token_id = str(uuid.uuid4())
        expiration_time = payload.get('exp')
        # await self.redis_manager.delete(full_id)
        await self.redis_manager.delete(token_id)
        # await self.redis_manager.set_string_data(f"{token_id}:{user_id}", token, expiration_time)
        await self.redis_manager.set_string_data(f"{new_token_id}", token, expiration_time)
        access_token = await self.issue_access_token(payload["sub"], payload["role"])
        data = {
            "accessToken": access_token,
            "exp": expiration_time,
            "tokenId": new_token_id
        }
        return data
