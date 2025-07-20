from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext


class QuitMiddleware(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        state: FSMContext = data.get("state")
        state = await self.state.get_state()
        if state is not None:
            result = await handler(event, data)
            return result
