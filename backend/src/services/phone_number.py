from typing import Union
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository
from src.schemas.phone_number import PhoneNumberBody, ValidatePhoneNumberBody, IsVerifiedPhoneNumberBody
from src.utils.code import code_manager
from src.bot.bot import bot
from src.enums.validation import ValidationEnum

class PhoneNumberService(Service):
    def __init__(
        self,
        session: AsyncSession,
        telegram_user_repo: Repository,
        user_repo: Repository
        ):
        super().__init__(session)
        self.telegram_user_repo = telegram_user_repo
        self.user_repo = user_repo
        self.code_manager = code_manager
        
    async def send(self, data: PhoneNumberBody) -> Union[list[dict, str], tuple[int, str]]:
        phone_number = data.get("phoneNumber")
        user = await self.telegram_user_repo(self.session).get_one_by_phone_number(phone_number)
        if not user:
            return (422, "Phone number has not found. You need to authorize it in telegram @exhange_v2_bot")
        if user.userId is not None:
            return (422, "Phone number has already taken")
        code = self.code_manager.make_code()
        id = str(uuid.uuid4())
        await self.redis_manager.set_string_data(f"phone-{id}:{phone_number}", str(code), ValidationEnum.EXPIRE_TIME.value)
        # CELERY 
        await bot.app.send_message(chat_id=user.chatId, text=f"Verification code: {code}")
        data["expirationTime"] = ValidationEnum.EXPIRE_TIME
        return [data, id]
    
    async def validate(self, user_id: int, validation_id: str, data: ValidatePhoneNumberBody) -> Union[dict, tuple[int, str]]:
        phone_number = data.get("phoneNumber")
        user = await self.telegram_user_repo(self.session).get_one_by_phone_number(phone_number)
        if not user:
            return (422, "Phone number has not found. You need to authorize it in telegram @exhange_v2_bot")
        redis_key = f"phone-{validation_id}:{phone_number}"
        code = await self.redis_manager.get_string_data(redis_key)
        if not code:
            return (400, "Validation id or phone number has not found")
        code = int(code)
        if data.get("code") != code:
            return (422, "Invalid verification code")
        # await self.telegram_user_repo(self.session).update_one(phone_number, userId=user_id)
        await self.redis_manager.delete(redis_key)
        await self.redis_manager.set_string_data(f"verified-phone:{user_id}", phone_number, ValidationEnum.EXPIRE_TIME.value)
        return {
            "phoneNumber": phone_number,
            "verified": True
        }
    
    async def is_verified(self, user_id: int, data: IsVerifiedPhoneNumberBody) -> Union[dict, tuple[int, str]]:
        phone_number = data.get("phoneNumber")
        data = await self.redis_manager.get_string_data(f"verified-phone:{user_id}")
        if not data:
            return (400, "Phone number is not verified")
        if data != phone_number:
            return (400, "Phone number is not verified")
        return {
            "verified": True,
            "phoneNumber": phone_number
        }
