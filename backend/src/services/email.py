from typing import Union
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.schemas.email import EmailBody, ValidateEmailBody, IsVerifiedEmailBody
from src.utils.repository import Repository
from src.utils.code import code_manager
from src.utils.email import email_manager
from src.enums.validation import ValidationEnum


class EmailService(Service):
    def __init__(
        self,
        session: AsyncSession,
        user_repo: Repository
        ):
        super().__init__(session)
        self.user_repo = user_repo
        self.code_manager = code_manager
        self.email_manager = email_manager
        
    async def send(self, data: EmailBody) -> Union[list[dict, str], tuple[int, str]]:
        email = data.get('email')
        # user = await self.user_repo(self.session).get_one_by_email(email)
        # if user:
        #     return (422, "Email has already found")
        code = code_manager.make_code()
        id = str(uuid.uuid4())
        await self.redis_manager.set_string_data(f"email-{id}:{email}", str(code), ValidationEnum.EXPIRE_TIME.value)
        # CELERY
        try:
            await self.email_manager.send_verification(email, code)
        except Exception:
            return (422, "Cannot send verification code. Email is invalid")
        data["expirationTime"] = ValidationEnum.EXPIRE_TIME
        return [data, id]
    
    async def validate(self, validation_id: str, data: ValidateEmailBody) -> Union[dict, tuple[int, str]]:
        email = data.get('email')
        # user = self.user_repo(self.session).get_one_by_email(email)
        # if user:
        #     return (422, "Email has already found")
        redis_key = f"email-{validation_id}:{email}"
        code = await self.redis_manager.get_string_data(redis_key)
        if not code:
            return (400, "Validation id or email has not found")
        code = int(code)
        if data.get("code") != code:
            return (422, "Invalid verification code")
        await self.redis_manager.delete(redis_key)
        await self.redis_manager.set_string_data(f"verified-email:{email}", email, ValidationEnum.EXPIRE_TIME.value)
        return {
            "email": email,
            "verified": True
        }
    
    async def is_verified(self, data: IsVerifiedEmailBody) -> Union[bool, tuple[int, str]]:
        email = data.get("email")
        data = await self.redis_manager.get_string_data(f"verified-email:{email}")
        if not data:
            return (400, "Email is not verified")
        if data != email:
            return (400, "Email is not verified")
        return {
            "verified": True,
            "email": email
        }
