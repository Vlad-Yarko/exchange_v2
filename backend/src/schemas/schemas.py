from typing import Optional
import datetime

from pydantic import Field

from src.utils.schema import Schema


class PaginationSchema(Schema):
    page: Optional[int] = Field(None, examples=[1], ge=1)
    count: int = Field(..., examples=[1], ge=0)
    hasNext: bool = Field(..., examples=[False])
    total: int = Field(..., examples=[1], ge=0)


class PublicSchema(Schema):
    id: int = Field(..., examples=[1])
    createdAt: datetime.datetime = Field(..., examples=["2025-07-02T00:28:57.553668"])
    updatedAt: datetime.datetime = Field(..., examples=["2025-07-02T00:28:57.553668"])
    
    model_config = {
        "extra": "ignore"
    }

