from pydantic import Field, field_validator

from src.utils.schema import Schema
from src.schemas import PaginationSchema, PublicSchema
from src.utils.validation import check_upper_case


class Currency(Schema):
    symbol1: str = Field(..., examples=["USDT"], min_length=1, max_length=20)
    symbol2: str = Field(..., examples=["UAH"], min_length=1, max_length=20)
    
    @field_validator("symbol1")
    def validate_symbol1(value):
        return check_upper_case(value)
    
    @field_validator("symbol2")
    def validate_symbol2(value):
        return check_upper_case(value)


class CurrencyBody(Currency):
    pass


class CurrencyPublic(Currency, PublicSchema):
    pass


class CurrenciesPublic(PaginationSchema):
    data: list[CurrencyPublic]
