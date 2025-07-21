from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class Email422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Email is invalid"])


class ValidateEmail422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Verification code is invalid"])
