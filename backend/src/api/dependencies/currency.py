from typing import Annotated, Callable, Awaitable

from fastapi import Depends, Path, HTTPException

from src.api.utils.dependency_factory import DependencyFactory
from src.api.dependencies.db import DBSession
from src.repositories import CurrencyRepository, CurrencySubscribeRepository, UserRepository
from src.clients import CurrencyClient
from src.services import CurrencyService
from src.schemas.currency import CurrencyBody, CurrencyPublic, CurrenciesPublic, CurrencySubscribeBody, CurrencySubscribePublic, CurrencySubscribesPublic, CurrencyPricePublic, CurrencyPriceBody
from src.models import User
from src.utils.validation import check_upper_case


async def service_dep(session: DBSession) -> CurrencyService:
    return CurrencyService(
        session=session,
        currency_client=CurrencyClient(),
        currency_repo=CurrencyRepository,
        currency_subscribes_repo=CurrencySubscribeRepository,
        user_repo=UserRepository
    )


class CurrencyDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=CurrencyBody,
            SchemaPublic=CurrencyPublic,
            DataSchemaPublic=CurrenciesPublic
        )
        
    def symbol_dep(self) -> Callable[[], Awaitable[str]]:
        async def dep(
            symbol: str = Path(..., examples=["USDUAH"], min_length=2, max_length=50, description="Unique symbol combination. 💫")
            ) -> str:
            try:
                check_upper_case(symbol)
            except ValueError:
                raise HTTPException(
                    status_code=422,
                    detail="Symbol must be in upper case"
                )
            return symbol
        return dep
    
    def get_price_dep(self) -> Callable[[], Awaitable[CurrencyPricePublic]]:
        async def dep(
            body: CurrencyPriceBody,
            user: User = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep)) -> CurrencyPricePublic:
            data = await service.get_price(body.model_dump())
            self.check_for_exception(data)
            response = CurrencyPricePublic(**data)
            return response
        return dep
        
    def subscribe_get_dep(self) -> Callable[[], Awaitable[CurrencySubscribesPublic]]:
        async def dep(
            user: User = Depends(self.token_dep()),
            page: int = Depends(self.page_dep()),
            service: CurrencyService = Depends(self.service_dep)) -> CurrencySubscribesPublic:
            data = await service.subscribes_get(user.id, page)
            response = CurrencySubscribesPublic(**data)
            return response
        return dep
        
    def subscribe_get_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            user: User = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep),
            symbol: str = Depends(self.symbol_dep())):
            data = await service.subscribe_get_one(user.id, symbol)
            self.check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
        
    def subscribe_create_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            body: CurrencyBody,
            user: User = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep)) -> CurrencySubscribeBody:
            data = await service.subscribe_create_one(user.id, body.model_dump())
            self.check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
    
    def subscribe_update_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            body: CurrencyBody,
            admin: User = Depends(self.admin_dep()),
            service: CurrencyService = Depends(self.service_dep),
            symbol: str = Depends(self.symbol_dep())) -> CurrencySubscribeBody:
            data = await service.subscribe_update_one(admin.id, symbol, body.model_dump())
            self.check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
    
    def subscribe_delete_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            user: User = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep),
            symbol: str = Depends(self.symbol_dep())) -> CurrencySubscribeBody:
            data = await service.subscribe_delete_one(user.id, symbol)
            self.check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
        
        
dependencies = CurrencyDependencyFactory()


# Prices

CurrencyPrice = Annotated[CurrencyPricePublic, Depends(dependencies.get_price_dep())]

# CRUDs
Currencies = Annotated[CurrenciesPublic, Depends(dependencies.get_dep())]
Currency = Annotated[CurrencyPublic, Depends(dependencies.get_one_dep())]
CreatedCurrency = Annotated[CurrencyPublic, Depends(dependencies.create_one_dep())]
UpdatedCurrency = Annotated[CurrencyPublic, Depends(dependencies.update_one_dep())]
DeletedCurrency = Annotated[CurrencyPublic, Depends(dependencies.delete_one_dep())]

# Subscribe CRUDs

CurrencySubscribes = Annotated[CurrencySubscribesPublic, Depends(dependencies.subscribe_get_dep())]
CurrencySubscribe = Annotated[CurrencySubscribePublic, Depends(dependencies.subscribe_get_one_dep())]
CreatedCurrencySubscribe = Annotated[CurrencySubscribePublic, Depends(dependencies.subscribe_create_one_dep())]
UpdatedCurrencySubscribe = Annotated[CurrencySubscribePublic, Depends(dependencies.subscribe_update_one_dep())]
DeletedCurrencySubscribe = Annotated[CurrencySubscribePublic, Depends(dependencies.subscribe_delete_one_dep())]
