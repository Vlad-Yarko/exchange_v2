from src.utils.schema import Schema
from src.schemas import PaginationSchema


class Currency(Schema):
    pass


class CurrencyBody(Schema):
    pass


class CurrencyPublic(Schema):
    pass


class CurrenciesPublic(PaginationSchema):
    data: list[CurrencyPublic]
