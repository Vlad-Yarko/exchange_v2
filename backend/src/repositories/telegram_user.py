from src.utils.repository import SQLAlchemyRepository
from src.models import TelegramUser


class TelegramUserRepository(SQLAlchemyRepository):
    model = TelegramUser
