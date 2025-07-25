from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction


class TelegramAuthorizeService(Service):
    def __init__(
        self,
        session: AsyncSession,
        telegram_user_repo: Repository
        ):
        super().__init__(session)
        self.telegram_user_repo = telegram_user_repo
        self.repo = telegram_user_repo
        
    async def get_one(self, chat_id: int, phone_number: str) -> Optional[dict]:
        data = await self.telegram_user_repo(self.session).get_one_by_chat_id_phone_number(chat_id, phone_number)
        return data.to_dict() if data else None
        
    @transaction
    async def create_one(self, data: dict) -> bool:
        user = await self.get_one(data["chatId"], data["phoneNumber"])
        if not user:
            await super().create_one(data)
            return True
        return False
