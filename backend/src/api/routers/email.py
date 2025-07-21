from fastapi import APIRouter

from src.api.dependencies.email import SentEmail, ValidatedEmail
from src.schemas.email import EmailPublic, ValidateEmailPublic, Email422, ValidateEmail422


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
