from typing import Union

from pydantic import Field

from src.utils.exception_schema import ExceptionSchema
    
    
class Authentication403(ExceptionSchema):
    detail: Union[str, dict] = Field(examples=["Not authenticated"])
