from fastapi import APIRouter

from src.api.dependencies.phone_number import SentPhoneNumber, ValidatedPhoneNumber, IsVerifiedPhoneNumber
from src.schemas.phone_number import PhoneNumberPublic, ValidatePhoneNumberPublic, IsVerifiedPhoneNumberPublic, PhoneNumber422, ValidatePhoneNumber422, IsVerifiedPhoneNumber422


router = APIRouter(
    prefix='/phone_numbers',
    tags=["PHONE_NUMBERs💫"]
)


@router.post("",
            summary="Sends code. 💫",
            description="**Sends** phone_number **verification** code. 💫",
            response_model=PhoneNumberPublic,
            responses={
                422: {'model': PhoneNumber422}
            })
async def send_phone_number_hand(data: SentPhoneNumber):
    return data


@router.post('/validate',
            summary="Validates code. 💫",
            description="**Validates** phone_number **verification** code. 💫",
            response_model=ValidatePhoneNumberPublic,
            responses={
                422: {'model': ValidatePhoneNumber422}
            })
async def validate_phone_number_hand(data: ValidatedPhoneNumber):
    return data


@router.post('/verified',
            summary="Check phone_number for verification. 💫",
            description="**Check** if phone_number is **verified**. 💫",
            response_model=IsVerifiedPhoneNumberPublic,
            responses={
                422: {'model': IsVerifiedPhoneNumber422}
            })
async def verified_phone_number_hand(data: IsVerifiedPhoneNumber):
    return data
