from sqlalchemy import String, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Crypto(Base):
    __tablename__ = 'crypto'

    symbol: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    symbol1: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol2: Mapped[str] = mapped_column(String(50), nullable=False)
    
    subscribes: Mapped[list["CryptoSubscribe"]] = relationship("CryptoSubscribe", back_populates="crypto", uselist=True)
    
    # __table_args__ = (
    #     PrimaryKeyConstraint("symbol1", "symbol2", name="crypto_symbol_ck"),
    # )

