from typing import Annotated, Callable, Awaitable, Optional, Union
import uuid

from fastapi import Depends, HTTPException, status, Cookie, Response, Path, Query

from src.api.utils.dependency_factory import DependencyFactory
from src.api.dependencies.db import DBSession
from src.repositories import UserRepository, TelegramUserRepository
from src.services import UserService
from src.schemas.user import UserBody, UserPublic, UsersPublic, LoginUserBody, LoginUserPublic, RefreshPublic, UpdateUserBody, LogoutUserPublic
from src.enums.user import TokenEnum
from src.models import User as UserModel

from src.utils.logger import logger


async def service_dep(session: DBSession) -> UserService:
    return UserService(
        session=session,
        user_repo=UserRepository,
        telegram_user_repo=TelegramUserRepository
    )


class UserDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=UserBody,
            SchemaPublic=UserPublic,
            DataSchemaPublic=UsersPublic,
            PhoneNumberBody=UpdateUserBody
        )
        
    def refresh_token_dep(self) -> uuid.UUID:
        async def dep(
            refreshToken: Optional[uuid.UUID] = Cookie(None, examples=[None], description="Refresh token id. (You do not need to pass it). 💫")            
        ) -> uuid.UUID:
            return refreshToken
        return dep
        
    def get_dep(self) -> Callable[[], Awaitable[UsersPublic]]:
        async def dep(
            admin: UserModel = Depends(self.admin_dep()),
            page: int = Depends(self.page_dep()),
            service: UserService = Depends(self.service_dep)) -> UsersPublic:
            data = await service.get(page)
            response = UsersPublic(**data)
            return response
        return dep
        
    def get_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            user: UserModel = Depends(self.token_dep()),
            service: UserService = Depends(self.service_dep)) -> UserPublic:
            data = await service.get_one(user.id)
            self.check_for_exception(data)
            response = UserPublic.model_validate(data, from_attributes=True)
            return response
        return dep
        
    def create_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        self.email_schema = UserBody
        async def dep(
            body: UserBody,
            service: UserService = Depends(self.service_dep),
            email: bool = Depends(self.verified_email_dep())) -> UserPublic:
            data = await service.create_one(body.model_dump())
            self.check_for_exception(data)
            response = UserPublic(**data)
            return response
        return dep


    def update_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        self.email_schema = UpdateUserBody
        self.phone_number_schema = UpdateUserBody
        async def dep(
            body: UpdateUserBody,
            user: UserModel = Depends(self.token_dep()),
            service: UserService = Depends(self.service_dep),
            email: bool = Depends(self.verified_email_dep()),
            phone_number: bool = Depends(self.verified_phone_number_dep())) -> UserPublic:
            data = await service.update_one(user.id, body.model_dump())
            self.check_for_exception(data)
            response = UserPublic(**data)
            return response
        return dep
    
    def delete_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            admin: UserModel = Depends(self.admin_dep()),
            service: UserService = Depends(self.service_dep),
            id: int = Path(..., examples=[1], description="Unique identifier of an object. 💫", ge=1)) -> UserPublic:
            data = await service.delete_one(id)
            self.check_for_exception(data)
            response = UserPublic(**data)
            return response
        return dep
    
    def login_user_dep(self) -> Callable[[], Awaitable[LoginUserPublic]]:
        async def dep(
            response: Response,
            body: LoginUserBody,
            service: UserService = Depends(self.service_dep),
            refreshToken: uuid.UUID = Depends(self.refresh_token_dep())) -> LoginUserPublic:
            if refreshToken:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is authenticated. Refresh token has found"
                )
            data = await service.login_user(body.model_dump())
            self.check_for_exception(data)
            self.set_cookie(response, "refreshToken", data.get("tokenId"), TokenEnum.REFRESH_TOKEN_EXP.value)
            return LoginUserPublic.model_validate(data.get('user'), from_attributes=True)
        return dep
    
    def logout_user_dep(self) -> Callable[[], Awaitable[Union[UserPublic, LogoutUserPublic]]]:
        async def dep(
            response: Response,
            service: UserService = Depends(self.service_dep),
            refresh_token: uuid.UUID = Depends(self.refresh_token_dep())
            ) -> UserPublic:
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is not authorized. Refresh token has not found"
                )
            data = await service.logout_user(str(refresh_token))
            self.check_for_exception(data)
            self.delete_cookie(response, "refreshToken")
            return UserPublic(**data) if data else LogoutUserPublic(message="OK")
        return dep
            
    
    def refresh_user_dep(self) -> Callable[[], Awaitable[RefreshPublic]]:
        async def dep(
            response: Response,
            service: UserService = Depends(self.service_dep),
            refresh_token: uuid.UUID = Depends(self.refresh_token_dep())) -> RefreshPublic:
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is not authorized. Refresh token has not found"
                )
            data = await service.refresh_user(str(refresh_token))
            self.check_for_exception(data)
            self.set_cookie(response, "refreshToken", data.get("tokenId"), data.get("exp"))
            return RefreshPublic(accessToken=data.get("accessToken"))
        return dep


dependencies = UserDependencyFactory()


# CRUDs
Users = Annotated[UsersPublic, Depends(dependencies.get_dep())]
User = Annotated[UserPublic, Depends(dependencies.get_one_dep())]
CreatedUser = Annotated[UserPublic, Depends(dependencies.create_one_dep())]
UpdatedUser = Annotated[UserPublic, Depends(dependencies.update_one_dep())]
DeletedUser = Annotated[UserPublic, Depends(dependencies.delete_one_dep())]

# Authentication
LoggedInUser = Annotated[UsersPublic, Depends(dependencies.login_user_dep())]
LoggedOutUser = Annotated[UserPublic, Depends(dependencies.logout_user_dep())]
RefreshedToken = Annotated[RefreshPublic, Depends(dependencies.refresh_user_dep())]
