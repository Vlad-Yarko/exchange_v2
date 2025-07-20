from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.utils.response import MessageResponse
from src.bot.text.register import *


class RegisterMessageResponse(MessageResponse):
    async def register_contact_hand(self, session: AsyncSession) -> None:
        # chat_id = self.message.chat.id
        # user = await TelegramUser.is_user_by_chat_id(session, chat_id)
        # if user:
        #     self.text = register_error.render()
        # else:
        #     await TelegramUser.register_tg_user(
        #         session,
        #         chat_id=chat_id,
        #         phone_number=self.message.contact.phone_number
        #     )
        #     self.text = register_success.render()

        # await self.state.clear()
        # await self.answer()
        pass
