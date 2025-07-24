from typing import Optional, Union
import uuid

from src.utils.repository import SQLAlchemyRepository
from src.models import CurrencySubscribe


class CurrencySubscribeRepository(SQLAlchemyRepository):
    model = CurrencySubscribe
    
    async def get_one_by_id_symbol(self, user_id: Union[int, uuid.UUID], symbol: str) -> Optional[CurrencySubscribe]:
        data = await self.get_one(userId=user_id, symbol=symbol)
        return data
