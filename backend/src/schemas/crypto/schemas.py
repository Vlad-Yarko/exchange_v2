from pydantic import Field, field_validator

from src.utils.schema import Schema
from src.schemas import PaginationSchema, PublicSchema
from src.utils.validation import check_upper_case


class Crypto(Schema):
    symbol1: str = Field(..., examples=["BTC"], min_length=1, max_length=20)
    symbol2: str = Field(..., examples=["USDT"], min_length=1, max_length=20)
    
    @field_validator("symbol1")
    def validate_symbol1(value):
        return check_upper_case(value)
    
    @field_validator("symbol2")
    def validate_symbol2(value):
        return check_upper_case(value)


class CryptoBody(Crypto):
    pass


class CryptoPublic(Crypto, PublicSchema):
    symbol: str = Field(..., examples=["BTCUSDT"])


class CryptoSPublic(PaginationSchema):
    data: list[CryptoPublic]
    
    
class CryptoSubscribe(Crypto):
    userId: int = Field(..., examples=[1], ge=1)
    
    
class CryptoSubscribeBody(CryptoSubscribe):
    pass


class CryptoSubscribePublic(CryptoSubscribe, PublicSchema):
    symbol: str = Field(..., examples=["BTCUSDT"])
    symbolId: int = Field(..., examples=[1], ge=1)
    
    
class CryptoSubscribesPublic(PaginationSchema):
    data: list[CryptoSubscribePublic]
    
    
class CryptoPrice(Schema):
    pass
    
    
class CryptoPriceBody(CryptoPrice):
    symbol1: str = Field(..., examples=["BTC"], min_length=1, max_length=20)
    symbol2: str = Field(..., examples=["USDT"], min_length=1, max_length=20)
    
    @field_validator("symbol1")
    def validate_symbol1(value):
        return check_upper_case(value)
    
    @field_validator("symbol2")
    def validate_symbol2(value):
        return check_upper_case(value)


class CryptoPricePublic(CryptoPrice):
    symbol: str = Field(examples=["TONUSDT"])
    price: float = Field(..., examples=[3.600000])
