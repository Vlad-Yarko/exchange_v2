from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class Email422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Email is invalid"])
    
    
class ValidateEmail400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Validation id or email has not found"])


class ValidateEmail422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Verification code is invalid"])
    
    
class IsVerifiedEmail400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["email is not verified"])


class IsVerifiedEmail422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Email is invalid"])
