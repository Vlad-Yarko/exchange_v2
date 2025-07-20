from fastapi import APIRouter

from src.schemas.crypto import CryptoPublic, CryptoSPublic
from src.schemas import Authentication403
from src.api.dependencies.crypto import CryptoS, Crypto, CreatedCrypto, UpdatedCrypto, DeletedCrypto


router = APIRouter(
    prefix='/crypto'
)


@router.get("",
            summary="Gets crypto currencies",
            description="Gets **crypto** currencies from database with their information via pagination",
            tags=["Crypto CRUDs"],
            response_model=CryptoSPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: CryptoS):
    return data


@router.get("/{id}",
            summary="Gets crypto currency",
            description="Gets **crypto** currency from database with its information",
            tags=["Crypto CRUDs"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: Crypto):
    return data


@router.post("",
            summary="Creates crypto currency",
            description="Creates **crypto** currency in database with its information",
            tags=["Crypto CRUDs"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: CreatedCrypto):
    return data


@router.put("",
            summary="Updates crypto currency",
            description="Updates **crypto** currency in database",
            tags=["Crypto CRUDs"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: UpdatedCrypto):
    return data


@router.delete("",
            summary="Deletes crypto currency",
            description="Deletes **crypto** currency from database",
            tags=["Crypto CRUDs"],
            response_model=CryptoPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: DeletedCrypto):
    return data
