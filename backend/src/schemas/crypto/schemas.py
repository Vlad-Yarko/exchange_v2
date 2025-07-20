from src.utils.schema import Schema
from src.schemas import PaginationSchema


class Crypto(Schema):
    pass


class CryptoBody(Schema):
    pass


class CryptoPublic(Schema):
    pass


class CryptoSPublic(PaginationSchema):
    data: list[CryptoPublic]
