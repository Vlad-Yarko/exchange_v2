from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.utils.response import MessageResponse
from src.bot.text.authorize import *
from src.services.telegram_authorize import TelegramAuthorizeService
from src.repositories import TelegramUserRepository


class AuthorizeMessageResponse(MessageResponse):
    async def authorize_contact_hand(self, session: AsyncSession) -> None:
        service = TelegramAuthorizeService(session, TelegramUserRepository)
        user_data = {
            "chatId": self.message.chat.id,
            "phoneNumber": self.message.contact.phone_number
            }
        data = await service.create_one(user_data)
        if not data:
            self.text = authorize_error_text.render()
        else:
            self.text = authorize_success_text.render()
        await self.state.clear()
        await self.answer()
