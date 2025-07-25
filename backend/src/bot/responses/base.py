from src.bot.utils.response import MessageResponse
from src.bot.text.base import *
from src.bot.keyboards.reply.authorize import authorize_keyboard
from src.bot.fsm import AuthorizeState


class BaseMessageResponse(MessageResponse):
    async def start_hand(self):
        self.text = start_hand_text.render(username=self.message.from_user.username)
        await self.answer()

    async def help_hand(self):
        self.text = help_hand_text.render()
        await self.answer()

    async def authorize_hand(self):
        self.text = authorize_hand_text.render()
        self.keyboard = authorize_keyboard
        await self.state.set_state(AuthorizeState.active)
        await self.answer()
