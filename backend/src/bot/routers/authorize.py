from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.responses.authorize import AuthorizeMessageResponse
from src.bot.fsm import AuthorizeState
from src.bot.filters.authorize import AuthorizeStateFilter, ContactFilter


router = Router()
router.message.filter(StateFilter(AuthorizeState))


@router.message(AuthorizeStateFilter('active'), ContactFilter())
async def register_contact_hand(message: Message, state: FSMContext, session: AsyncSession):
    print("LDKDK")
    await AuthorizeMessageResponse(
        message=message,
        state=state
    ).authorize_contact_hand(session)
