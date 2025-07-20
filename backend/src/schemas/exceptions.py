from pydantic import Field

from src.utils.exception_schema import ExceptionSchema
    
    
class Authentication403(ExceptionSchema):
    detail: str = Field(examples=["Not authenticated"])
