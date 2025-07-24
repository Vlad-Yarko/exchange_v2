from typing import Annotated

from fastapi import Depends

from src.api.utils.validation_factory import ValidationDependencyFactory
from src.services import PhoneNumberService
from src.schemas.phone_number import PhoneNumberPublic, PhoneNumberBody, ValidatePhoneNumberPublic, ValidatePhoneNumberBody, IsVerifiedPhoneNumberBody, IsVerifiedPhoneNumberPublic


async def service_dep() -> PhoneNumberService:
    return PhoneNumberService()


class PhoneNumberDependencyFactory(ValidationDependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            ValidationBody=PhoneNumberBody,
            ValidationPublic=PhoneNumberPublic,
            ValidateValidationBody=ValidatePhoneNumberBody,
            ValidateValidationPublic=ValidatePhoneNumberPublic,
            IsVerifiedValidationBody=IsVerifiedPhoneNumberBody,
            IsVerifiedValidationPublic=IsVerifiedPhoneNumberPublic
        )
            

dependencies = PhoneNumberDependencyFactory()


SentPhoneNumber = Annotated[PhoneNumberPublic, Depends(dependencies.send_dep())]
ValidatedPhoneNumber = Annotated[ValidatePhoneNumberPublic, Depends(dependencies.validate_dep())]
IsVerifiedPhoneNumber = Annotated[IsVerifiedPhoneNumberPublic, Depends(dependencies.is_verified_dep())]
