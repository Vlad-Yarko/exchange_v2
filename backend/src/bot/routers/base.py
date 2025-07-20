from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from src.bot.responses.base import BaseMessageResponse


router = Router()
router.message.filter(StateFilter(None))


@router.message(Command('start'))
async def start_hand(message: Message, state: FSMContext):
    await BaseMessageResponse(
        message=message,
        state=state
    ).start_hand()


@router.message(Command('help'))
async def help_hand(message: Message, state: FSMContext):
    await BaseMessageResponse(
        message=message,
        state=state
    ).help_hand()


@router.message(Command('register'))
async def register_hand(message: Message, state: FSMContext):
    await BaseMessageResponse(
        message=message,
        state=state
    ).register_hand()
