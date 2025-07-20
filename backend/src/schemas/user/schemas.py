from src.utils.schema import Schema
from src.schemas import PaginationSchema


class User(Schema):
    pass


class UserBody(Schema):
    pass


class UserPublic(Schema):
    pass


class UsersPublic(PaginationSchema):
    data: list[UserPublic]
