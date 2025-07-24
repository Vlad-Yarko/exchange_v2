from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

# from src.utils.db_manager import DatabaseManager
from src.databases.mysql_manager import db_session


class DBSession(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        async for session in db_session():
            data['session'] = session
            result = await handler(event, data)
            return result
