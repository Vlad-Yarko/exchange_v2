from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class GetUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])


class CreateUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Phone number is invalid"])
    
    
class UpdateUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
    
    
class DeleteUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
