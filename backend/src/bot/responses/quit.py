from src.bot.utils.response import MessageResponse
from src.bot.text.quit import quit_hand_text


class QuitMessageResponse(MessageResponse):
    async def quit_hand(self):
        await self.state.clear()
        self.text = quit_hand_text.render()
        self.keyboard = {"remove_keyboard": True}
        await self.answer()
