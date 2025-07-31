from typing import Annotated, Callable, Awaitable

from fastapi import Depends, Path, HTTPException

from src.api.utils.dependency_factory import DependencyFactory
from src.api.dependencies.db import DBSession
from src.repositories import CryptoRepository, CryptoSubscribeRepository, UserRepository
from src.clients import CryptoClient
from src.services import CryptoService
from src.schemas.crypto import CryptoBody, CryptoPublic, CryptoSPublic, CryptoSubscribeBody, CryptoSubscribePublic, CryptoSubscribesPublic, CryptoPricePublic, CryptoPriceBody
from src.models import User
from src.utils.validation import check_upper_case


async def service_dep(session: DBSession) -> CryptoService:
    return CryptoService(
        session=session,
        crypto_client=CryptoClient(),
        crypto_repo=CryptoRepository,
        crypto_subscribes_repo=CryptoSubscribeRepository,
        user_repo=UserRepository
    )


class CryptoDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=CryptoBody,
            SchemaPublic=CryptoPublic,
            DataSchemaPublic=CryptoSPublic
        )
        
    def symbol_dep(self) -> Callable[[], Awaitable[str]]:
        async def dep(
            symbol: str = Path(..., examples=["BTCUSDT"], min_length=2, max_length=50, description="Unique symbol combination. 💫")
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
        
    def get_price_dep(self) -> Callable[[], Awaitable[CryptoPricePublic]]:
        async def dep(
            body: CryptoPriceBody,
            user: User = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep)) -> CryptoPricePublic:
            data = await service.get_price(body.model_dump())
            self.check_for_exception(data)
            response = CryptoPricePublic(**data)
            return response
        return dep
        
    def subscribe_get_dep(self) -> Callable[[], Awaitable[CryptoSubscribesPublic]]:
        async def dep(
            user: User = Depends(self.token_dep()),
            page: int = Depends(self.page_dep()),
            service: CryptoService = Depends(self.service_dep)) -> CryptoSubscribesPublic:
            data = await service.subscribes_get(user.id, page)
            response = CryptoSubscribesPublic(**data)
            return response
        return dep
        
    def subscribe_get_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            user: User = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep),
            symbol: str = Depends(self.symbol_dep())):
            data = await service.subscribe_get_one(user.id, symbol)
            self.check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
        
    def subscribe_create_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            body: CryptoBody,
            user: User = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep)) -> CryptoSubscribeBody:
            data = await service.subscribe_create_one(user.id, body.model_dump())
            self.check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
    
    def subscribe_update_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            body: CryptoBody,
            admin: User = Depends(self.admin_dep()),
            service: CryptoService = Depends(self.service_dep),
            symbol: str = Depends(self.symbol_dep()),
            ) -> CryptoSubscribeBody:
            data = await service.subscribe_update_one(admin.id, symbol, body.model_dump())
            self.check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
    
    def subscribe_delete_one_dep(self) -> Callable[[], Awaitable[CryptoSubscribePublic]]:
        async def dep(
            user: User = Depends(self.token_dep()),
            service: CryptoService = Depends(self.service_dep),
            symbol: str = Depends(self.symbol_dep())) -> CryptoSubscribeBody:
            data = await service.subscribe_delete_one(user.id, symbol)
            self.check_for_exception(data)
            response = CryptoSubscribePublic(**data)
            return response
        return dep
        
        
dependencies = CryptoDependencyFactory()


# Prices

CryptoPrice = Annotated[CryptoPricePublic, Depends(dependencies.get_price_dep())]

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

