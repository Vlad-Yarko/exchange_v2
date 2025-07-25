from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    chatId: Mapped[int] = mapped_column(BigInteger, nullable=False)
    phoneNumber: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    userId: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="telegram_user", uselist=False)
