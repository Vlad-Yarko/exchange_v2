from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class GetCurrency422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])


class CreateCurrency422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Symbols combination has already found"])
    
    
class UpdateCurrency422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
    
    
class DeleteCurrency422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
