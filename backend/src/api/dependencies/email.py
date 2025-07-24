from typing import Annotated, Callable, Awaitable

from fastapi import Depends, HTTPException

from src.api.utils.validation_factory import ValidationDependencyFactory
from src.services import EmailService
from src.schemas.email import EmailPublic, EmailBody, ValidateEmailPublic, ValidateEmailBody, IsVerifiedEmailBody, IsVerifiedEmailPublic


async def service_dep() -> EmailService:
    return EmailService()


class EmailDependencyFactory(ValidationDependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            ValidationBody=EmailBody,
            ValidationPublic=EmailPublic,
            ValidateValidationBody=ValidateEmailBody,
            ValidateValidationPublic=ValidateEmailPublic,
            IsVerifiedValidationBody=IsVerifiedEmailBody,
            IsVerifiedValidationPublic=IsVerifiedEmailPublic
        )
            

dependencies = EmailDependencyFactory()


SentEmail = Annotated[EmailPublic, Depends(dependencies.send_dep())]
ValidatedEmail = Annotated[ValidateEmailPublic, Depends(dependencies.validate_dep())]
IsVerifiedEmail = Annotated[IsVerifiedEmailPublic, Depends(dependencies.is_verified_dep())]
