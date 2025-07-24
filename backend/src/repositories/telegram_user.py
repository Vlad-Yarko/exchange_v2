from typing import Optional, Union
import uuid

from src.utils.repository import SQLAlchemyRepository
from src.models import TelegramUser


class TelegramUserRepository(SQLAlchemyRepository):
    model = TelegramUser
    
    async def get_one_by_phone_number(self, phone_number: str) -> Optional[TelegramUser]:
        data = await self.get_one(phoneNumber=phone_number)
        return data
