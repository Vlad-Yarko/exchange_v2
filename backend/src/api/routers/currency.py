from fastapi import APIRouter

from src.schemas.currency import CurrencyPublic, CurrenciesPublic
from src.schemas import Authentication403
from src.api.dependencies.currency import Currencies, Currency, CreatedCurrency, UpdatedCurrency, DeletedCurrency


router = APIRouter(
    prefix='/currency'
)


@router.get("",
            summary="Gets currencies",
            description="Gets **world** currencies from database with their information via pagination",
            tags=["Currency CRUDs"],
            response_model=CurrenciesPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: Currencies):
    return data


@router.get("/{id}",
            summary="Gets world currency",
            description="Gets **world** currency from database with its information",
            tags=["Currency CRUDs"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_currency(data: Currency):
    return data


@router.post("",
            summary="Creates world currency",
            description="Creates **world** currency in database with its information",
            tags=["Currency CRUDs"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_currency(data: CreatedCurrency):
    return data


@router.put("",
            summary="Updates world currency",
            description="Updates **world** currency in database",
            tags=["Currency CRUDs"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_currency(data: UpdatedCurrency):
    return data


@router.delete("",
            summary="Deletes world currency",
            description="Deletes **world** currency from database",
            tags=["Currency CRUDs"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_currency(data: DeletedCurrency):
    return data
