from typing import Union, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction
from src.schemas.crypto import CryptoBody, CryptoSubscribeBody


class CryptoService(Service):
    def __init__(
        self,
        session: AsyncSession,
        crypto_repo: Repository,
        crypto_subscribes_repo: Repository
    ):
        super().__init__(session)
        self.repo = crypto_repo
        self.crypto_repo = crypto_repo
        self.crypto_subscribes_repo = crypto_subscribes_repo
        
    @transaction
    async def create_one(self, data: CryptoBody) -> Union[dict, tuple[int, str]]:
        symbol = data.get("symbol1") + data.get('symbol2')
        d = await self.crypto_repo(self.session).get_one_by_symbol(symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = symbol
        return await super().create_one(data)
    
    @transaction
    async def update_one(self, id: Union[int, uuid.UUID], data: CryptoBody) -> Union[dict, tuple[int, str]]:
        symbol = data.get("symbol1") + data.get('symbol2')
        d = await self.crypto_repo(self.session).get_one_by_symbol(symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = symbol
        return await super().update_one(id, data)
    
    @transaction
    async def delete_one(self, id: Union[int, uuid.UUID]) -> Union[dict, tuple[int, str]]:
        return await super().delete_one(id)
    
    async def subscribes_get(self, page: Optional[int] = None) -> dict:
        self.repo = self.crypto_subscribes_repo
        data = await super().get(page)
        self.repo = self.crypto_repo
        return data        
    
    async def subscribe_get_one(symbol: str) -> dict:
        pass
    
    @transaction
    async def subscribe_create_one(self, data: CryptoSubscribeBody) -> Union[dict, tuple[int, str]]:
        symbol = data.get("symbol1") + data.get('symbol2')
        d = await self.crypto_repo(self.session).get_one_by_symbol(symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = symbol
        return await super().create_one(data)
    
    @transaction
    async def subscribe_update_one(self, symbol: str, data: CryptoSubscribeBody) -> Union[dict, tuple[int, str]]:
        symbol = data.get("symbol1") + data.get('symbol2')
        d = await self.crypto_repo(self.session).get_one_by_symbol(symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = symbol
        return await super().update_one(id, data)
    
    @transaction
    async def subscribe_delete_one(self, symbol: str) -> Union[dict, tuple[int, str]]:
        return await super().delete_one(id)
