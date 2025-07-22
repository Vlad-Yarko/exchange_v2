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
    
    
class LoginUser400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["User is authenticated. Refresh token has found"])
    
    
class LoginUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Username has not found"])
    
    
class RefreshUser400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["User is not authenticated. Refresh token has not found"])
