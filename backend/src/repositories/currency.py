from typing import Optional

from src.utils.repository import SQLAlchemyRepository
from src.models import Currency


class CurrencyRepository(SQLAlchemyRepository):
    model = Currency
    
    async def get_one_by_symbol(self, symbol: str) -> Optional[Currency]:
        data = await self.get_one(symbol=symbol)
        return data
