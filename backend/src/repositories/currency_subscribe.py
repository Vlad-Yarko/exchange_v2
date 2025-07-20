from src.utils.repository import SQLAlchemyRepository
from src.models import CurrencySubscribe


class CurrencySubscribeRepository(SQLAlchemyRepository):
    model = CurrencySubscribe
