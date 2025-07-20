from typing import Annotated

from fastapi import Depends

from src.api.utils.dependency_factory import DependencyFactory
from src.api.dependencies.db import DBSession
from src.repositories import CurrencyRepository
from src.services import CurrencyService
from src.schemas.currency import CurrencyBody, CurrencyPublic, CurrenciesPublic


async def service_dep(session: DBSession) -> CurrencyService:
    return CurrencyService(
        session=session,
        currency_repo=CurrencyRepository
    )


class CurrencyDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=CurrencyBody,
            SchemaPublic=CurrencyPublic
        )
        
        
dependencies = CurrencyDependencyFactory()


# CRUDs
Currencies = Annotated[CurrenciesPublic, Depends(dependencies.get_dep())]
Currency = Annotated[CurrencyPublic, Depends(dependencies.get_one_dep())]
CreatedCurrency = Annotated[CurrencyPublic, Depends(dependencies.create_one_dep())]
UpdatedCurrency = Annotated[CurrencyPublic, Depends(dependencies.update_one_dep())]
DeletedCurrency = Annotated[CurrencyPublic, Depends(dependencies.delete_one_dep())]
