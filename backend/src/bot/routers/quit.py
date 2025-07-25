from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.responses.quit import QuitMessageResponse
from src.bot.filters.quit import QuitFilter
from src.bot.middlewares.quit import QuitMiddleware


router = Router()
router.message.filter(StateFilter('*'))
# router.message.middleware(QuitMiddleware())


@router.message(QuitFilter())
async def quit_hand(message: Message, state: FSMContext):
    await QuitMessageResponse(
        message=message,
        state=state
    ).quit_hand()
