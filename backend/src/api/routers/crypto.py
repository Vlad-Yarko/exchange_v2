from fastapi import APIRouter

from src.schemas.crypto import *
from src.schemas import Authentication403
from src.api.dependencies.crypto import CryptoPrice, CryptoS, Crypto, CreatedCrypto, UpdatedCrypto, DeletedCrypto, CryptoSubscribes, CryptoSubscribe, CreatedCryptoSubscribe, UpdatedCryptoSubscribe, DeletedCryptoSubscribe


router = APIRouter(
    prefix='/crypto'
)


@router.post("/price",
            summary="Gets price. 💫 (Protected🗝️)",
            description="Gets **current** crypto currency price by symbol. 💫",
            tags=["Market_data💫"],
            response_model=CryptoPricePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetCryptoPrice422}
            })
async def get_crypto_price(data: CryptoPrice):
    return data


@router.get("/subscribes",
            summary="Gets crypto subscribes. 💫 (Protected🗝️)",
            description="Gets user **crypto** subscribes from database with their information via pagination. 💫",
            tags=["Crypto_subscribes_CRUDs💫"],
            response_model=CryptoSubscribesPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto_subscribes(data: CryptoSubscribes):
    return data


@router.get("/subscribes/{symbol}",
            summary="Gets crypto subscribe. 💫 (Protected🗝️)",
            description="Gets user **crypto** subscribe from database with its information. 💫",
            tags=["Crypto_subscribes_CRUDs💫"],
            response_model=CryptoSubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetCryptoSubscribe422}
            })
async def get_crypto_subscribe(data: CryptoSubscribe):
    return data


@router.post("/subscribes",
            summary="Creates crypto subscribe. 💫 (Protected🗝️)",
            description="Creates user **crypto** subscribe in database with its information. 💫",
            tags=["Crypto_subscribes_CRUDs💫"],
            response_model=CryptoSubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': CreateCryptoSubscribe422}
            })
async def create_crypto_subscribe(data: CreatedCryptoSubscribe):
    return data


@router.put("/subscribes/{symbol}",
            summary="Updates crypto subscribe. 💫 (Admins-only⚙️)",
            description="Updates user **crypto** subscribe in database. 💫",
            tags=["Crypto_subscribes_CRUDs💫"],
            response_model=CryptoSubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': UpdateCryptoSubscribe422}
            })
async def update_crypto_subscribe(data: UpdatedCryptoSubscribe):
    return data


@router.delete("/subscribes/{symbol}",
            summary="Deletes crypto subscribe. 💫 (Protected🗝️)",
            description="Deletes user **crypto** subscribe from database. 💫",
            tags=["Crypto_subscribes_CRUDs💫"],
            response_model=CryptoSubscribePublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': DeleteCryptoSubscribe422}
            })
async def delete_crypto_subscribe(data: DeletedCryptoSubscribe):
    return data


@router.get("",
            summary="Gets crypto currencies. 💫 (Protected🗝️)",
            description="Gets **crypto** currencies from database with their information via pagination. 💫",
            tags=["Crypto_CRUDs💫"],
            response_model=CryptoSPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_cryptos(data: CryptoS):
    return data


@router.get("/{id}",
            summary="Gets crypto currency. 💫 (Protected🗝️)",
            description="Gets **crypto** currency from database with its information. 💫",
            tags=["Crypto_CRUDs💫"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetCrypto422}
            })
async def get_crypto(data: Crypto):
    return data


@router.post("",
            summary="Creates crypto currency. 💫 (Admins-only⚙️)",
            description="Creates **crypto** currency in database with its information. 💫",
            tags=["Crypto_CRUDs💫"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': CreateCrypto422}
            })
async def create_crypto(data: CreatedCrypto):
    return data


@router.put("/{id}",
            summary="Updates crypto currency. 💫 (Admins-only⚙️)",
            description="Updates **crypto** currency in database. 💫",
            tags=["Crypto_CRUDs💫"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': UpdateCrypto422}
            })
async def update_crypto(data: UpdatedCrypto):
    return data


@router.delete("/{id}",
            summary="Deletes crypto currency. 💫 (Admins-only⚙️)",
            description="Deletes **crypto** currency from database. 💫",
            tags=["Crypto_CRUDs💫"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': DeleteCrypto422}
            })
async def delete_crypto(data: DeletedCrypto):
    return data
