import re

from pydantic import Field, EmailStr, field_validator

from src.utils.schema import Schema
from src.schemas import PublicSchema


class Email(Schema):
    email: EmailStr = Field(..., examples=["mister_business@gmail.com"])


class EmailBody(Email):
    pass


class EmailPublic(Email):
    expirationTime: int = Field(..., examples=[300])


class ValidateEmail(Schema):
    email: EmailStr = Field(..., examples=["mister_business@gmail.com"])


class ValidateEmailBody(ValidateEmail):
    code: int = Field(..., examples=[123456])
    
    @field_validator("code")
    def validate_code(value):
        if not re.fullmatch(r"^\d{6}$", str(value)):
            raise ValueError("Code must be 6-digit")
        return value


class ValidateEmailPublic(ValidateEmail):
    verified: bool = Field(examples=[True])


class IsVerifiedEmail(Email):
    pass
    
    
class IsVerifiedEmailBody(IsVerifiedEmail):
    email: EmailStr = Field(..., examples=["mister_business@gmail.com"])
    
    
class IsVerifiedEmailPublic(IsVerifiedEmail):
    verified: bool = Field(examples=[True])

