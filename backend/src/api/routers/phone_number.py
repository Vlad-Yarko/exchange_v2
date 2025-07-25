from fastapi import APIRouter

from src.api.dependencies.phone_number import SentPhoneNumber, ValidatedPhoneNumber, IsVerifiedPhoneNumber
from src.schemas import Authentication403
from src.schemas.phone_number import PhoneNumberPublic, ValidatePhoneNumberPublic, IsVerifiedPhoneNumberPublic, ValidatePhoneNumber400, PhoneNumber422, ValidatePhoneNumber422, IsVerifiedPhoneNumber400, IsVerifiedPhoneNumber422


router = APIRouter(
    prefix='/phone_numbers',
    tags=["PHONE_NUMBERs💫"]
)


@router.post("",
            summary="Sends code. 💫 (Protected🗝️)",
            description="**Sends** phone_number **verification** code. 💫",
            response_model=PhoneNumberPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': PhoneNumber422}
            })
async def send_phone_number_hand(data: SentPhoneNumber):
    return data


@router.post('/validate',
            summary="Validates code. 💫 (Protected🗝️)",
            description="**Validates** phone_number **verification** code. 💫",
            response_model=ValidatePhoneNumberPublic,
            responses={
                400: {'model': ValidatePhoneNumber400},
                403: {'model': Authentication403},
                422: {'model': ValidatePhoneNumber422}
            })
async def validate_phone_number_hand(data: ValidatedPhoneNumber):
    return data


@router.post('/verified',
            summary="Check phone_number for verification. 💫 (Protected🗝️)",
            description="**Check** if phone_number is **verified**. 💫",
            response_model=IsVerifiedPhoneNumberPublic,
            responses={
                400: {'model': IsVerifiedPhoneNumber400},
                403: {'model': Authentication403},
                422: {'model': IsVerifiedPhoneNumber422}
            })
async def verified_phone_number_hand(data: IsVerifiedPhoneNumber):
    return data
