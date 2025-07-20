from aiogram.types import Message
from aiogram.filters import Filter


class QuitFilter(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        return message.text == '/quit' or message.text == 'quit'
