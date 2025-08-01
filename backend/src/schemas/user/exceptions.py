from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema


class GetUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
    
    
class CreateUser400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Email is not verified"])


class CreateUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Username has already found"])
    
    
class UpdateUser400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Email is not verified"])
    
    
class UpdateUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
    
    
class DeleteUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Id has not found"])
    
    
class GoogleUrl400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["User is not authorized. Refresh token has not found"])
    
    
class GoogleCallback400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["User is not authorized. Refresh token has not found"])
    

class GoogleCallback422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Invalid google code has sent"])
    
    
class LoginUser400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["User is not authorized. Refresh token has not found"])
    
    
class LoginUser422(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["Username has not found"])
    
    
class LogoutUser400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["User is not authorized. Refresh token has not found"])
    
    
class RefreshUser400(ExceptionSchema):
    detail: Union[str, dict] = Field(..., examples=["User is not authenticated. Refresh token has not found"])
