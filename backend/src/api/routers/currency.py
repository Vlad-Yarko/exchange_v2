from fastapi import APIRouter

from src.schemas.currency import CurrencyPublic, CurrenciesPublic, CurrencySubscribePublic, CurrencySubscribesPublic, GetCurrency422, CreateCurrency422, UpdateCurrency422, DeleteCurrency422, GetCurrencySubscribe422, CreateCurrencySubscribe422, DeleteCurrencySubscribe422, UpdateCurrencySubscribe422
from src.schemas import Authentication403
from src.api.dependencies.currency import Currencies, Currency, CreatedCurrency, UpdatedCurrency, DeletedCurrency, CurrencySubscribes, CurrencySubscribe, CreatedCurrencySubscribe, UpdatedCurrencySubscribe, DeletedCurrencySubscribe


router = APIRouter(
    prefix='/currency'
)


@router.get("",
            summary="Gets world currencies. 💫 (Protected🗝️)",
            description="Gets **world** currencies from database with their information via pagination. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrenciesPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_currencies(data: Currencies):
    return data


@router.get("/{id}",
            summary="Gets world currency. 💫 (Protected🗝️)",
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
            summary="Creates world currency. 💫 (Admins-only⚙️)",
            description="Creates **world** currency in database with its information. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': CreateCurrency422}
            })
async def create_currency(data: CreatedCurrency):
    return data


@router.put("/{id}",
            summary="Updates world currency. 💫 (Admins-only⚙️)",
            description="Updates **world** currency in database. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': UpdateCurrency422}
            })
async def update_currency(data: UpdatedCurrency):
    return data


@router.delete("/{id}",
            summary="Deletes world currency. 💫 (Admins-only⚙️)",
            description="Deletes **world** currency from database. 💫",
            tags=["Currency_CRUDs💫"],
            response_model=CurrencyPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': DeleteCurrency422}
            })
async def delete_currency(data: DeletedCurrency):
    return data


@router.get("/subscribes",
            summary="Gets currency subscribes. 💫 (Protected🗝️)",
            description="Gets user **currency** subscribes from database with their information via pagination. 💫",
            tags=["Currency_subscribes_CRUDs💫"],
            response_model=CurrencySubscribesPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_currency_subscribes(data: CurrencySubscribes):
    return data


@router.get("/subscribes/{symbol}",
            summary="Gets currency subscribe. 💫 (Protected🗝️)",
            description="Gets user **currency** subscribe from database with its information. 💫",
            tags=["Currency_subscribes_CRUDs💫"],
            response_model=CurrencySubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetCurrencySubscribe422}
            })
async def get_currency_subscribe(data: CurrencySubscribe):
    return data


@router.post("/subscribes",
            summary="Creates currency subscribe. 💫 (Protected🗝️)",
            description="Creates user **currency** subscribe in database with its information. 💫",
            tags=["Currency_subscribes_CRUDs💫"],
            response_model=CurrencySubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': CreateCurrencySubscribe422}
            })
async def create_currency_subscribe(data: CreatedCurrencySubscribe):
    return data


@router.put("/subscribes/{symbol}",
            summary="Updates currency subscribe. 💫 (Admins-only⚙️)",
            description="Updates user **currency** subscribe in database. 💫",
            tags=["Currency_subscribes_CRUDs💫"],
            response_model=CurrencySubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': UpdateCurrencySubscribe422}
            })
async def update_currency_subscribe(data: UpdatedCurrencySubscribe):
    return data


@router.delete("/subscribes/{symbol}",
            summary="Deletes currency subscribe. 💫 (Protected🗝️)",
            description="Deletes user **currency** subscribe from database. 💫",
            tags=["Currency_subscribes_CRUDs💫"],
            response_model=CurrencySubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': DeleteCurrencySubscribe422}
            })
async def delete_currency_subscribe(data: DeletedCurrencySubscribe):
    return data
