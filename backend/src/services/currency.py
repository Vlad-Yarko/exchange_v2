from typing import Union
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction
from src.schemas.currency import CurrencyBody


class CurrencyService(Service):
    def __init__(
        self,
        session: AsyncSession,
        currency_repo: Repository
    ):
        super().__init__(session)
        self.repo = currency_repo
        self.currency_repo = currency_repo
        
    @transaction
    async def create_one(self, data: CurrencyBody) -> Union[dict, tuple[int, str]]:
        symbol = data.get("symbol1") + data.get('symbol2')
        d = await self.currency_repo(self.session).get_one_by_symbol(symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = symbol
        return await super().create_one(data)
    
    @transaction
    async def update_one(self, id: Union[int, uuid.UUID], data: CurrencyBody) -> Union[dict, tuple[int, str]]:
        symbol = data.get("symbol1") + data.get('symbol2')
        d = await self.currency_repo(self.session).get_one_by_symbol(symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = symbol
        return await super().update_one(id, data)
    
    @transaction
    async def delete_one(self, id: Union[int, uuid.UUID]) -> Union[dict, tuple[int, str]]:
        return await super().delete_one(id)
