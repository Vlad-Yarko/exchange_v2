from typing import Optional

from src.utils.repository import SQLAlchemyRepository
from src.models import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_one_by_username(self, username: str) -> Optional[User]:
        data = await self.get_one(username=username)
        return data
    
    async def get_one_by_email(self, email: str) -> Optional[User]:
        data = await self.get_one(email=email)
        return data
