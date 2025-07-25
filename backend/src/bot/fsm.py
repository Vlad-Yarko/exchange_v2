from aiogram.fsm.state import StatesGroup, State


class AuthorizeState(StatesGroup):
    active = State()
