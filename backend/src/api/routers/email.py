from fastapi import APIRouter

from src.api.dependencies.email import SentEmail, ValidatedEmail, IsVerifiedEmail
from src.schemas.email import EmailPublic, ValidateEmailPublic, IsVerifiedEmailPublic, Email422, ValidateEmail422, IsVerifiedEmail422


router = APIRouter(
    '/emails',
    tags=["EMAILs💫"]
)


@router.post("",
            summary="Sends code. 💫",
            description="**Sends** email **verification** code. 💫",
            response_model=EmailPublic,
            responses={
                422: {'model': Email422}
            })
async def send_email_hand(data: SentEmail):
    return data


@router.post('/validate',
            summary="Validates code. 💫",
            description="**Validates** email **verification** code. 💫",
            response_model=ValidateEmailPublic,
            responses={
                422: {'model': ValidateEmail422}
            })
async def validate_email_hand(data: ValidatedEmail):
    return data


@router.post('/verified',
            summary="Check email for verification. 💫",
            description="**Check** if email is **verified**. 💫",
            response_model=IsVerifiedEmailPublic,
            responses={
                422: {'model': IsVerifiedEmail422}
            })
async def validate_email_hand(data: IsVerifiedEmail):
    return data
