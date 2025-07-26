from typing import Callable, Awaitable, Optional, Annotated

from fastapi import Depends, Response, Cookie, HTTPException

from src.api.dependencies.db import DBSession
from src.schemas.phone_number import PhoneNumberBody, PhoneNumberPublic, ValidatePhoneNumberBody, ValidatePhoneNumberPublic, IsVerifiedPhoneNumberBody, IsVerifiedPhoneNumberPublic
from src.repositories import TelegramUserRepository, UserRepository
from src.api.utils.dependency_factory import DependencyFactory
from src.services import PhoneNumberService
from src.enums.validation import ValidationEnum
from src.models import User


async def service_dep(session: DBSession) -> PhoneNumberService:
    return PhoneNumberService(
        session=session,
        telegram_user_repo=TelegramUserRepository,
        user_repo=UserRepository
    )


class PhoneNumberDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
        )
        
    def send_dep(self) -> Callable[[], Awaitable[PhoneNumberPublic]]:
        async def dep(
            response: Response,
            body: PhoneNumberBody,
            user: User = Depends(self.token_dep()),
            service: PhoneNumberService = Depends(self.service_dep)) -> PhoneNumberPublic:
            data = await service.send(body.model_dump())
            self.check_for_exception(data)
            self.set_cookie(response, "phoneNumber", data[1], ValidationEnum.EXPIRE_TIME.value) 
            return PhoneNumberPublic(**data[0])
        return dep
    
    def validate_dep(self) -> Callable[[], Awaitable[ValidatePhoneNumberPublic]]:
        async def dep(
            response: Response,
            body: ValidatePhoneNumberBody,
            user: User = Depends(self.token_dep()),
            service: PhoneNumberService = Depends(self.service_dep),
            phoneNumber: Optional[str] = Cookie(None, examples=[None], description="Validation id. (You do not need to pass it). 💫")) -> ValidatePhoneNumberPublic:
            if not phoneNumber:
                raise HTTPException(
                    status_code=400,
                    detail="Validation id has not found"
                )
            data = await service.validate(user.id, phoneNumber, body.model_dump())
            self.check_for_exception(data)
            self.delete_cookie(response, phoneNumber)
            return ValidatePhoneNumberPublic(**data)
        return dep
    
    def is_verified_dep(self) -> Callable[[], Awaitable[IsVerifiedPhoneNumberPublic]]:
        async def dep(
            body: IsVerifiedPhoneNumberBody,
            user: User = Depends(self.token_dep()),
            service: PhoneNumberService = Depends(self.service_dep)) -> IsVerifiedPhoneNumberPublic:
            data = await service.is_verified(user.id, body.model_dump())
            self.check_for_exception(data)
            response = IsVerifiedPhoneNumberPublic(**data)
            return response
        return dep
    
    
dependencies = PhoneNumberDependencyFactory()


SentPhoneNumber = Annotated[PhoneNumberPublic, Depends(dependencies.send_dep())]
ValidatedPhoneNumber = Annotated[ValidatePhoneNumberPublic, Depends(dependencies.validate_dep())]
IsVerifiedPhoneNumber = Annotated[IsVerifiedPhoneNumberPublic, Depends(dependencies.is_verified_dep())]
