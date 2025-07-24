from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class CurrencySubscribe(Base):
    __tablename__ = 'currency_subscribes'

    symbol: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol1: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol2: Mapped[str] = mapped_column(String(50), nullable=False)

    userId: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    symbolId: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete="CASCADE"))
    
    currency: Mapped["Currency"] = relationship("Currency", back_populates="subscribes", uselist=False)

