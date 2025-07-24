from typing import Optional

from src.utils.repository import SQLAlchemyRepository
from src.models import Crypto


class CryptoRepository(SQLAlchemyRepository):
    model = Crypto
    
    async def get_one_by_symbol(self, symbol: str) -> Optional[Crypto]:
        data = await self.get_one(symbol=symbol)
        return data
