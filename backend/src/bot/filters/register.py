from aiogram.types import Message
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext


class ContactFilter(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        return message.contact is not None


class RegisterStateFilter(Filter):
    def __init__(self, state_name):
        self.state_name = state_name

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state() == f'RegisterState:{self.state_name}'
