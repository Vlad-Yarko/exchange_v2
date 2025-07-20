from src.bot.utils.response import MessageResponse
from src.bot.text.base import *
from src.bot.keyboards.reply.register_reply import register_keyboard
from src.bot.fsm import RegisterState


class BaseMessageResponse(MessageResponse):
    async def start_hand(self):
        self.text = start_hand_text.render(username=self.message.from_user.username)
        await self.answer()

    async def help_hand(self):
        self.text = help_hand_text.render()
        await self.answer()

    async def register_hand(self):
        self.text = register_hand_text.render()
        self.keyboard = register_keyboard
        await self.state.set_state(RegisterState.active)
        await self.answer()
