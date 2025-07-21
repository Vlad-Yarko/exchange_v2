import re

from pydantic import Field, EmailStr, field_validator

from src.utils.schema import Schema
from src.schemas import PublicSchema


class Email(Schema):
    email: EmailStr


class EmailBody(Email):
    pass


class EmailPublic(Email, PublicSchema):
    pass


class ValidateEmail(Schema):
    email: EmailStr
    verified: bool = Field(examples=[True])


class ValidateEmailBody(ValidateEmail):
    code: int = Field(..., examples=[123456])
    
    @field_validator("code")
    def validate_code(value):
        if not re.fullmatch(r"^\d{6}$"):
            raise ValueError("Code must be 6-digit")
        return value


class ValidateEmailPublic(ValidateEmail, PublicSchema):
    pass


class IsVerifiedEmail(Schema):
    pass
    
    
class IsVerifiedEmailBody(IsVerifiedEmail):
    email: EmailStr
    
    
class IsVerifiedEmailPublic(IsVerifiedEmail):
    verified: bool = Field(examples=[True])

