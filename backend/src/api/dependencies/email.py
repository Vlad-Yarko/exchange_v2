from typing import Annotated, Callable, Awaitable

from fastapi import Depends, HTTPException

from src.api.utils.dependency_factory import DependencyFactory, check_for_exception
from src.services import EmailService
from src.schemas.email import EmailPublic, EmailBody, ValidateEmailPublic, ValidateEmailBody, IsVerifiedEmailBody, IsVerifiedEmailPublic


async def service_dep() -> EmailService:
    return EmailService()


class EmailDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
        )
        
    def send_email_dep(self) -> Callable[[], Awaitable[EmailPublic]]:
        async def dep(
            body: EmailBody,
            service: EmailService = Depends(self.service_dep)) -> EmailPublic:
            data = await service.send_email(body.model_dump())
            check_for_exception(data)
            response = EmailPublic(**data)
            return response
        return dep
    
    def validate_email_dep(self) -> Callable[[], Awaitable[ValidateEmailPublic]]:
        async def dep(
            body: ValidateEmailBody,
            service: EmailService = Depends(self.service_dep)) -> ValidateEmailPublic:
            data = await service.validate_email(body.model_dump())
            check_for_exception(data)
            response = ValidateEmailPublic(**data)
            return response
        return dep
    
    def is_verified_email_dep(self) -> Callable[[], Awaitable[IsVerifiedEmailPublic]]:
        async def dep(
            body: IsVerifiedEmailBody,
            service: EmailService = Depends(self.service_dep)) -> IsVerifiedEmailPublic:
            data = await service.is_verified_email(body.email)
            response = IsVerifiedEmailPublic(**data)
            return response
        return dep
            

dependencies = EmailDependencyFactory()


SentEmail = Annotated[EmailPublic, Depends(dependencies.send_email_dep())]
ValidatedEmail = Annotated[ValidateEmailPublic, Depends(dependencies.validate_email_dep())]
IsVerifiedEmail = Annotated[IsVerifiedEmailPublic, Depends(dependencies.is_verified_email_dep())]
