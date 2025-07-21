from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class GetCrypto422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])


class CreateCrypto422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Symbols combination has already found"])
    
    
class UpdateCrypto422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
    
    
class DeleteCrypto422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
