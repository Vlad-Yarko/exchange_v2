from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.enums.user import RoleEnum


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phoneNumber: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    role: Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum, name="user_role_enum", native_enum=False), default=RoleEnum.USER)
    # phoneNumber: Mapped[str] = mapped_column(ForeignKey('telegram_users.phoneNumber'), nullable=False, unique=True)
    
    telegram_user: Mapped["TelegramUser"] = relationship("TelegramUser", back_populates="user", uselist=False)
