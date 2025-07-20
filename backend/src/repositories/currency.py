from src.utils.repository import SQLAlchemyRepository
from src.models import Currency


class CurrencyRepository(SQLAlchemyRepository):
    model = Currency
