import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class CryptoSubscribe(Base):
    __tablename__ = 'crypto_subscribes'

    symbol: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol1: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol2: Mapped[str] = mapped_column(String(50), nullable=False)

    userId: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    symbolId: Mapped[uuid.UUID] = mapped_column(ForeignKey('crypto.id', ondelete="CASCADE"))
    
    crypto: Mapped["Crypto"] = relationship("Crypto", back_populates="subscribes", uselist=False)
