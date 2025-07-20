from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    
    createdAt: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updatedAt: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
