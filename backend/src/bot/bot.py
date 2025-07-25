from aiogram import Bot as AiogramBot, Dispatcher

from src.utils.application import Application
from src.config import settings
from src.bot.commands import commands
from src.bot.routers import *
from src.bot.middlewares import DBSession


class Bot(Application):
    def __init__(self):
        super().__init__()
        self.token = settings.BOT_TOKEN
        self.dp = Dispatcher()
        self.dp.message.middleware(DBSession())
        self.dp.callback_query.middleware(DBSession())
        self.commands = commands
        self.routers = [
            base_router,
            register_router,
            quit_router
        ]
        self.dp.include_routers(*self.routers)
        
    def create(self) -> AiogramBot:
        self.app = AiogramBot(
            token=self.token
        )
        return self.app
    
    async def run(self) -> None:
        await self.app.set_my_commands(commands=self.commands)
        await self.dp.start_polling(self.app, allowed_updates=self.dp.resolve_used_update_types())
        
        
bot = Bot()
bot.create()
