from typing import Annotated, Callable, Awaitable, Optional

from fastapi import Depends, Query, Path

from src.api.utils.dependency_factory import DependencyFactory, check_for_exception
from src.api.dependencies.db import DBSession
from src.repositories import CurrencyRepository, CurrencySubscribeRepository
from src.services import CurrencyService
from src.schemas.currency import CurrencyBody, CurrencyPublic, CurrenciesPublic, CurrencySubscribeBody, CurrencySubscribePublic, CurrencySubscribesPublic


async def service_dep(session: DBSession) -> CurrencyService:
    return CurrencyService(
        session=session,
        currency_repo=CurrencyRepository,
        currency_subscribes_repo=CurrencySubscribeRepository
    )


class CurrencyDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=CurrencyBody,
            SchemaPublic=CurrencyPublic,
            DataSchemaPublic=CurrenciesPublic
        )
        
        
    def subscribe_get_dep(self) -> Callable[[], Awaitable[CurrencySubscribesPublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            page: Optional[int] = Query(None, examples=[1], description="Number of pagination page. 💫", ge=1),
            service: CurrencyService = Depends(self.service_dep)) -> CurrencySubscribesPublic:
            data = await service.subscribes_get(page)
            response = CurrencySubscribesPublic(**data)
            return response
        return dep
        
    def subscribe_get_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep),
            symbol: str = Path(..., examples=["BTCUSD"], min_length=2, max_length=50, description="Unique symbol combination. 💫")):
            data = await service.subscribe_get_one(symbol)
            check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
        
    def subscribe_create_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            body: CurrencyBody,
            token: str = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep)) -> CurrencySubscribeBody:
            data = await service.subscribe_create_one(body.model_dump())
            check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
    
    def subscribe_update_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            body: CurrencyBody,
            token: str = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep),
            symbol: str = Path(..., examples=["BTCUSD"], min_length=2, max_length=50, description="Unique symbol combination. 💫")) -> CurrencySubscribeBody:
            data = await service.subscribe_update_one(symbol, body.model_dump())
            check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
    
    def subscribe_delete_one_dep(self) -> Callable[[], Awaitable[CurrencySubscribePublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            service: CurrencyService = Depends(self.service_dep),
            symbol: str = Path(..., examples=["BTCUSD"], min_length=2, max_length=50, description="Unique symbol combination. 💫")) -> CurrencySubscribeBody:
            data = await service.subscribe_update_one(symbol)
            check_for_exception(data)
            response = CurrencySubscribePublic(**data)
            return response
        return dep
        
        
dependencies = CurrencyDependencyFactory()


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
