from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.utils.db_manager import DatabaseManager


class DBSession(BaseMiddleware):
    def __init__(self, sessionmaker: DatabaseManager):
        self.sessionmaker = sessionmaker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        async with self.sessionmaker() as session:
            data['session'] = session
            result = await handler(event, data)
            return result
