import re

from pydantic import Field, field_validator

from src.utils.schema import Schema
from src.utils.validation import check_phone_number


class PhoneNumber(Schema):
    phoneNumber: str = Field(..., examples=["+380999999999"])
    
    @field_validator("phoneNumber")
    def validate_phone_number(value):
        return check_phone_number(value)


class PhoneNumberBody(PhoneNumber):
    pass


class PhoneNumberPublic(PhoneNumber):
    expirationTime: int = Field(..., examples=[300])


class ValidatePhoneNumber(PhoneNumber):
    pass


class ValidatePhoneNumberBody(PhoneNumber):
    code: int = Field(..., examples=[123456])
    
    @field_validator("code")
    def validate_code(value):
        if not re.fullmatch(r"^\d{6}$", str(value)):
            raise ValueError("Code must be 6-digit")
        return value


class ValidatePhoneNumberPublic(ValidatePhoneNumber):
    verified: bool = Field(examples=[True])


class IsVerifiedPhoneNumber(PhoneNumber):
    pass
    
    
class IsVerifiedPhoneNumberBody(IsVerifiedPhoneNumber):
    pass
    
    
class IsVerifiedPhoneNumberPublic(IsVerifiedPhoneNumber):
    verified: bool = Field(examples=[True])
