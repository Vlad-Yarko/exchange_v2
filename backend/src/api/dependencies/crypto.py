from typing import Annotated, Callable, Awaitable, Optional

from fastapi import Depends, Path, Query

from src.api.utils.dependency_factory import DependencyFactory, check_for_exception
from src.api.dependencies.db import DBSession
from src.repositories import CryptoRepository, CryptoSubscribeRepository
from src.services import CryptoService
from src.schemas.crypto import CryptoBody, CryptoPublic, CryptoSPublic, CryptoSubscribeBody, CryptoSubscribePublic, CryptoSubscribesPublic


async def service_dep(session: DBSession) -> CryptoService:
    return CryptoService(
        session=session,
        crypto_repo=CryptoRepository,
        crypto_subscribes_repo=CryptoSubscribeRepository
    )


class CryptoDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=CryptoBody,
            SchemaPublic=CryptoPublic,
            DataSchemaPublic=CryptoSPublic
        )
        
    def subscribe_get_dep(self) -> Callable[[], Awaitable[CryptoSubscribesPublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            page: Optional[int] = Query(None, examples=[1], description="Number of pagination page. 💫", ge=1),
            service: CryptoService = Depends(self.service_dep)) -> CryptoSubscribesPublic:
            data = await service.subscribes_get(page)
            response = CryptoSubscribesPublic(**data)
            return response
        return dep
        
    def subscribe_get_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep),
            symbol: str = Path(..., examples=["BTCUSD"], min_length=2, max_length=50, description="Unique symbol combination. 💫")):
            data = await service.subscribe_get_one(symbol)
            check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
        
    def subscribe_create_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            body: CryptoBody,
            token: str = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep)) -> CryptoSubscribeBody:
            data = await service.subscribe_create_one(body.model_dump())
            check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
    
    def subscribe_update_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            body: CryptoBody,
            token: str = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep),
            symbol: str = Path(..., examples=["BTCUSD"], min_length=2, max_length=50, description="Unique symbol combination. 💫")) -> CryptoSubscribeBody:
            data = await service.subscribe_update_one(symbol, body.model_dump())
            check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
    
    def subscribe_delete_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep),
            symbol: str = Path(..., examples=["BTCUSD"], min_length=2, max_length=50, description="Unique symbol combination. 💫")) -> CryptoSubscribeBody:
            data = await service.subscribe_update_one(symbol)
            check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
        
        
dependencies = CryptoDependencyFactory()


# CRUDs
CryptoS = Annotated[CryptoSPublic, Depends(dependencies.get_dep())]
Crypto = Annotated[CryptoPublic, Depends(dependencies.get_one_dep())]
CreatedCrypto = Annotated[CryptoPublic, Depends(dependencies.create_one_dep())]
UpdatedCrypto = Annotated[CryptoPublic, Depends(dependencies.update_one_dep())]
DeletedCrypto = Annotated[CryptoPublic, Depends(dependencies.delete_one_dep())]

# Subscribe CRUDs

CryptoSubscribes = Annotated[CryptoSubscribesPublic, Depends(dependencies.subscribe_get_dep())]
CryptoSubscribe = Annotated[CryptoSubscribePublic, Depends(dependencies.subscribe_get_one_dep())]
CreatedCryptoSubscribe = Annotated[CryptoSubscribePublic, Depends(dependencies.subscribe_create_one_dep())]
UpdatedCryptoSubscribe = Annotated[CryptoSubscribePublic, Depends(dependencies.subscribe_update_one_dep())]
DeletedCryptoSubscribe = Annotated[CryptoSubscribePublic, Depends(dependencies.subscribe_delete_one_dep())]

