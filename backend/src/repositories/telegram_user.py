from typing import Optional, Union

from sqlalchemy import update

from src.utils.repository import SQLAlchemyRepository
from src.models import TelegramUser


class TelegramUserRepository(SQLAlchemyRepository):
    model = TelegramUser
    
    async def get_one_by_phone_number(self, phone_number: str) -> Optional[TelegramUser]:
        data = await self.get_one(phoneNumber=phone_number)
        return data
    
    async def get_one_by_chat_id_phone_number(self, chat_id: int, phone_number: str) -> Optional[TelegramUser]:
        data = await self.get_one(chatId=chat_id, phoneNumber=phone_number)
        return data
    
    async def update_one_by_phone_number(self, phone_number: str, **kwargs) -> None:
        smtp = update(self.model).where(self.model.phoneNumber == phone_number).values(**kwargs)
        await self.session.execute(smtp)
