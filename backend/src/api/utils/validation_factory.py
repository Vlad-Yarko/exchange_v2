from typing import Callable, Awaitable, Optional

from fastapi import Depends, Response, Cookie, HTTPException

from src.api.utils.dependency_factory import DependencyFactory
from src.utils.service import Service
from src.types.validation_factory import (
    TValidationBody,
    TValidationPublic,
    TValidateValidationBody,
    TValidateValidationPublic,
    TIsVerifiedValidationBody,
    TIsVerifiedValidationPublic
)
from src.enums.validation import ValidationEnum


class ValidationDependencyFactory(DependencyFactory):
    def __init__(
        self,
        service_dep: Callable[[], Awaitable[Service]],
        cookie_name: str,
        ValidationBody: TValidationBody,
        ValidationPublic: TValidationPublic,
        ValidateValidationBody: TValidateValidationBody,
        ValidateValidationPublic: TValidateValidationPublic,
        IsVerifiedValidationBody: TIsVerifiedValidationBody,
        IsVerifiedValidationPublic: TIsVerifiedValidationPublic,):
        super().__init__(
            service_dep=service_dep,
        )
        self.cookie_name = cookie_name
        self.ValidationBody = ValidationBody
        self.ValidationPublic = ValidationPublic
        self.ValidateValidationBody = ValidateValidationBody
        self.ValidateValidationPublic = ValidateValidationPublic
        self.IsVerifiedValidationBody = IsVerifiedValidationBody
        self.IsVerifiedValidationPublic = IsVerifiedValidationPublic
        
    def send_dep(self) -> Callable[[], Awaitable[TValidationPublic]]:
        ValidationBody = self.ValidationBody
        async def dep(
            response: Response,
            body: ValidationBody,
            service: Service = Depends(self.service_dep)) -> TValidationPublic:
            data = await service.send(body.model_dump())
            self.check_for_exception(data)
            self.set_cookie(response, self.cookie_name, data[1], ValidationEnum.EXPIRE_TIME) 
            return self.ValidationPublic(**data[0])
        return dep
    
    def validate_dep(self) -> Callable[[], Awaitable[TValidateValidationPublic]]:
        ValidateValidationBody = self.ValidateValidationBody
        async def dep(
            body: ValidateValidationBody,
            service: Service = Depends(self.service_dep),
            validationCookie: Optional[str] = Cookie(None, examples=[None], alias=self.cookie_name), description="Validation id. (You do not need to pass it). 💫") -> TValidateValidationPublic:
            if not validationCookie:
                raise HTTPException(
                    status_code=400,
                    detail="Validation id has not found"
                )
            data = await service.validate(validationCookie, body.model_dump())
            self.check_for_exception(data)
            response = self.ValidateValidationPublic(**data)
            return response
        return dep
    
    def is_verified_dep(self) -> Callable[[], Awaitable[TIsVerifiedValidationPublic]]:
        IsVerifiedValidationBody = self.IsVerifiedValidationBody
        async def dep(
            body: IsVerifiedValidationBody,
            service: Service = Depends(self.service_dep)) -> TIsVerifiedValidationPublic:
            data = await service.is_verified(body.mode_dump())
            response = self.IsVerifiedValidationPublic(**data)
            return response
        return dep

