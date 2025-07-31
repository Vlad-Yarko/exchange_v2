from typing import Union, Optional
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction
from src.utils.client import JSONClient, http_session
from src.utils.decimal import format_decimal
from src.schemas.currency import CurrencyBody, CurrencySubscribeBody, CurrencyPriceBody


class CurrencyService(Service):
    def __init__(
        self,
        session: AsyncSession,
        currency_client: JSONClient,
        currency_repo: Repository,
        currency_subscribes_repo: Repository,
        user_repo: Repository
    ):
        super().__init__(session)
        self.repo = currency_repo
        self.currency_repo = currency_repo
        self.currency_subscribes_repo = currency_subscribes_repo
        self.user_repo = user_repo
        self.client = currency_client
        
    @http_session
    async def get_price(self, data: CurrencyPriceBody) -> Union[dict, tuple[int, str]]:
        symbol1 = data.get("symbol1")
        symbol2 = data.get("symbol2")
        symbol = symbol1 + symbol2
        symbol_data = await self.currency_repo(self.session).get_one_by_symbol(symbol)
        if not symbol_data:
            return (422, "Symbol combination has not found")
        client_data = await self.client.get_symbol_price(symbol1, symbol2)
        if not client_data:
            return (422, "Symbol combination has not found")
        data = dict()
        data["symbol"] = symbol
        price = float(client_data.get('quotes').get(symbol))
        data["price"] = format_decimal(price)        
        return data
            
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
    
    async def get_subscribe_one(self, user_id: Union[int, uuid.UUID], symbol: str) -> Union[dict, tuple[int, str]]:
        subscribe = await self.currency_subscribes_repo(self.session).get_one_by_id_symbol(user_id, symbol)
        if not subscribe:
            return (422, "Symbols combination has not found")
        return subscribe
    
    async def subscribes_get(self, user_id: Union[int, uuid.UUID], page: Optional[int] = None) -> dict:
        self.repo = self.currency_subscribes_repo
        data = await super().get(page, userId=user_id)
        self.repo = self.currency_repo
        return data   
    
    async def subscribe_get_one(self, user_id: Union[int, uuid.UUID], symbol: str) -> dict:
        subscribe = await self.get_subscribe_one(user_id, symbol)
        if isinstance(subscribe, tuple):
            return subscribe
        return subscribe.to_dict()
    
    @transaction
    async def subscribe_create_one(self, user_id: Union[int, uuid.UUID], data: CurrencySubscribeBody) -> Union[dict, tuple[int, str]]:
        symbol = data.get("symbol1") + data.get('symbol2')
        symbol_data = await self.currency_repo(self.session).get_one_by_symbol(symbol)
        if not symbol_data:
            return (422, "Symbols combination has not found")
        d = await self.currency_subscribes_repo(self.session).get_one_by_id_symbol(user_id, symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = symbol
        data['userId'] = user_id
        data['symbolId'] = symbol_data.id
        self.repo = self.currency_subscribes_repo
        data = await super().create_one(data)
        self.repo = self.currency_repo
        return data   
    
    @transaction
    async def subscribe_update_one(self, user_id: Union[int, uuid.UUID], symbol: str, data: CurrencySubscribeBody) -> Union[dict, tuple[int, str]]:
        new_symbol = data.get("symbol1") + data.get('symbol2')
        symbol_data = await self.currency_repo(self.session).get_one_by_symbol(new_symbol)
        if not symbol_data:
            return (422, "Symbols combination has not found")
        subscribe = await self.get_subscribe_one(user_id, symbol)
        if isinstance(subscribe, tuple):
            return subscribe
        d = await self.currency_subscribes_repo(self.session).get_one_by_id_symbol(user_id, new_symbol)
        if d:
            return (422, "Symbols combination has already found")
        data['symbol'] = new_symbol
        data['symbolId'] = symbol_data.id
        subscribe = await self.currency_subscribes_repo(self.session).update_one(subscribe.id, **data)
        return subscribe.to_dict()
    
    @transaction
    async def subscribe_delete_one(self, user_id: Union[int, uuid.UUID], symbol: str) -> Union[dict, tuple[int, str]]:
        subscribe = await self.get_subscribe_one(user_id, symbol)
        if isinstance(subscribe, tuple):
            return subscribe
        subscribe = await self.currency_subscribes_repo(self.session).delete_one(subscribe.id)
        return subscribe.to_dict()
