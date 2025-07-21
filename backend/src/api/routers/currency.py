from fastapi import APIRouter

from src.schemas.currency import CurrencyPublic, CurrenciesPublic, GetCurrency422, CreateCurrency422, UpdateCurrency422, DeleteCurrency422
from src.schemas import Authentication403
from src.api.dependencies.currency import Currencies, Currency, CreatedCurrency, UpdatedCurrency, DeletedCurrency


router = APIRouter(
    prefix='/currency'
)


@router.get("",
            summary="Gets currencies. 💫",
            description="Gets **world** currencies from database with their information via pagination. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrenciesPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: Currencies):
    return data


@router.get("/{id}",
            summary="Gets world currency. 💫",
            description="Gets **world** currency from database with its information. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetCurrency422}
            })
async def get_currency(data: Currency):
    return data


@router.post("",
            summary="Creates world currency. 💫",
            description="Creates **world** currency in database with its information. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': CreateCurrency422}
            })
async def get_currency(data: CreatedCurrency):
    return data


@router.put("/{id}",
            summary="Updates world currency. 💫",
            description="Updates **world** currency in database. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': UpdateCurrency422}
            })
async def get_currency(data: UpdatedCurrency):
    return data


@router.delete("/{id}",
            summary="Deletes world currency. 💫",
            description="Deletes **world** currency from database. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': DeleteCurrency422}
            })
async def get_currency(data: DeletedCurrency):
    return data
