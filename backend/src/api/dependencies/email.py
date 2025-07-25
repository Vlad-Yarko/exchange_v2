from typing import Annotated, Callable, Awaitable, Optional

from fastapi import Depends, HTTPException, Response, Cookie, HTTPException

from src.api.utils.validation_factory import ValidationDependencyFactory
from src.services import EmailService
from src.schemas.email import EmailPublic, EmailBody, ValidateEmailPublic, ValidateEmailBody, IsVerifiedEmailBody, IsVerifiedEmailPublic
from src.api.utils.dependency_factory import DependencyFactory
from src.enums.validation import ValidationEnum


async def service_dep() -> EmailService:
    return EmailService()


class EmailDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
        )
        
    def send_dep(self) -> Callable[[], Awaitable[EmailPublic]]:
        async def dep(
            response: Response,
            body: EmailBody,
            service: EmailService = Depends(self.service_dep)) -> EmailPublic:
            data = await service.send(body.model_dump())
            self.check_for_exception(data)
            self.set_cookie(response, self.cookie_name, data[1], ValidationEnum.EXPIRE_TIME) 
            return EmailPublic(**data[0])
        return dep
    
    def validate_dep(self) -> Callable[[], Awaitable[ValidateEmailPublic]]:
        async def dep(
            body: ValidateEmailBody,
            service: EmailService = Depends(self.service_dep),
            validationCookie: Optional[str] = Cookie(None, examples=[None], description="Validation id. (You do not need to pass it). 💫")) -> ValidateEmailPublic:
            if not validationCookie:
                raise HTTPException(
                    status_code=400,
                    detail="Validation id has not found"
                )
            data = await service.validate(validationCookie, body.model_dump())
            self.check_for_exception(data)
            response = ValidateEmailPublic(**data)
            return response
        return dep
    
    def is_verified_dep(self) -> Callable[[], Awaitable[IsVerifiedEmailPublic]]:
        async def dep(
            body: IsVerifiedEmailBody,
            service: EmailService = Depends(self.service_dep)) -> IsVerifiedEmailPublic:
            data = await service.is_verified(body.model_dump())
            self.check_for_exception(data)
            response = IsVerifiedEmailPublic(**data)
            return response
        return dep
            

dependencies = EmailDependencyFactory()


SentEmail = Annotated[EmailPublic, Depends(dependencies.send_dep())]
ValidatedEmail = Annotated[ValidateEmailPublic, Depends(dependencies.validate_dep())]
IsVerifiedEmail = Annotated[IsVerifiedEmailPublic, Depends(dependencies.is_verified_dep())]
