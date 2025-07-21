from typing import Annotated, Callable, Awaitable

from fastapi import Depends, HTTPException

from src.api.utils.dependency_factory import DependencyFactory
from src.services import EmailService
from src.schemas.email import EmailPublic, EmailBody, ValidateEmailPublic, ValidateEmailBody


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
            if isinstance(data, tuple):
                raise HTTPException(
                    status_code=data[0],
                    detail=data[1]
                )
            response = EmailPublic(**data)
            return response
        return dep
    
    def validate_email_dep(self) -> Callable[[], Awaitable[ValidateEmailPublic]]:
        async def dep(
            body: ValidateEmailBody,
            service: EmailService = Depends(self.service_dep)) -> ValidateEmailPublic:
            data = await service.validate_email(body.model_dump())
            if isinstance(data, tuple):
                raise HTTPException(
                    status_code=data[0],
                    detail=data[1]
                )
            response = ValidateEmailPublic(**data)
            return response
        return dep


dependencies = EmailDependencyFactory()


SentEmail = Annotated[EmailPublic, Depends(dependencies.send_email_dep())]
ValidatedEmail = Annotated[ValidateEmailPublic, Depends(dependencies.validate_email_dep())]
