from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class PhoneNumber422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Phone number is invalid"])


class ValidatePhoneNumber422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Verification code is invalid"])


class IsVerifiedPhoneNumber422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Phone number is invalid"])
