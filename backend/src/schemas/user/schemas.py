from typing import Optional
import re

from pydantic import Field, EmailStr, field_validator

from src.utils.schema import Schema
from src.schemas import PaginationSchema, PublicSchema
from src.enums.user import RoleEnum
from src.utils.validation import check_phone_number


class UserSchema(Schema):
    username: str = Field(..., examples=["mister_business"], min_length=2, max_length=25)
    email: EmailStr = Field(..., examples=["mister_business@gmail.com"])
    
    @field_validator("username")
    def validate_username(value):
        if not re.fullmatch(r"^[a-zA-Z][a-zA-Z0-9]*(?:[._]?[a-zA-Z0-9]+)*$", value):
            raise ValueError("""Username is invalid. It cannot contain special characters and cannot be ended with: ., _""")
        return value
    
    
class PasswordSchema(Schema):
    password: str = Field(..., examples=["12345678"], min_length=8, max_length=64)
    
    @field_validator("password")
    def validate_password(value):
        if not re.fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,64}$", value):
            raise ValueError("""Password is invalid. It must contain at least: one lowercase letter, one upper case letter, one digit, on special character. Length: 8-64""")
        return value


class User(UserSchema):
    phoneNumber: Optional[str] = Field(None, examples=["+380999999999"])
    
    @field_validator("phoneNumber")
    def validate_phone_number(value):
        return check_phone_number(value)


class UserBody(User, PasswordSchema):
    pass


class UserPublic(User, PublicSchema):
    role: RoleEnum = Field(..., examples=[RoleEnum.USER])


class UsersPublic(PaginationSchema):
    data: list[UserPublic]
    
    
class LoginUser(UserSchema):
    pass
    
    
class LoginUserBody(LoginUser, PasswordSchema):
    pass


class LoginUserPublic(LoginUser, PublicSchema):
    pass


class Refresh(Schema):
    pass


class RefreshPublic(Refresh):
    accessToken: str = Field(..., examples=['asfnbmbmbewrqdijhdsfafgsdhhvbxcbfgerydgsfgagf'])
