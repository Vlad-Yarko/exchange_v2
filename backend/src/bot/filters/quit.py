from aiogram.types import Message
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext


class QuitFilter(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        state_data = await state.get_state()
        result = state_data is not None and message.text == '/quit' or message.text == 'quit'
        return result
