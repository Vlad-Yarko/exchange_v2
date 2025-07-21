from typing import Annotated

from fastapi import Depends

from src.api.utils.dependency_factory import DependencyFactory
from src.api.dependencies.db import DBSession
from src.repositories import CryptoRepository
from src.services import CryptoService
from src.schemas.crypto import CryptoBody, CryptoPublic, CryptoSPublic


async def service_dep(session: DBSession) -> CryptoService:
    return CryptoService(
        session=session,
        crypto_repo=CryptoRepository
    )


class CryptoDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=CryptoBody,
            SchemaPublic=CryptoPublic,
            DataSchemaPublic=CryptoSPublic
        )
        
        
dependencies = CryptoDependencyFactory()


# CRUDs
CryptoS = Annotated[CryptoSPublic, Depends(dependencies.get_dep())]
Crypto = Annotated[CryptoPublic, Depends(dependencies.get_one_dep())]
CreatedCrypto = Annotated[CryptoPublic, Depends(dependencies.create_one_dep())]
UpdatedCrypto = Annotated[CryptoPublic, Depends(dependencies.update_one_dep())]
DeletedCrypto = Annotated[CryptoPublic, Depends(dependencies.delete_one_dep())]
