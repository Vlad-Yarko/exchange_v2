from typing import Optional, Union
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository, transaction
from src.utils.password import pw_manager
from src.utils.jwt import jwt_manager
from src.schemas.user import UserBody


class UserService(Service):
    def __init__(
        self,
        session: AsyncSession,
        user_repo: Repository
    ):
        super().__init__(session)
        self.repo = user_repo
        self.user_repo = user_repo
        self.jwt = jwt_manager
        self.pw = pw_manager
        
    async def issue_refresh_token(self, id: int, exp: Optional[int] = None) -> str:
        token = self.jwt.create_refresh_token(str(id), exp)
        return token
    
    async def issue_access_token(self, id: int) -> str:
        token = self.jwt.create_access_token(str(id))
        return token
    
    @transaction
    async def create_one(self, data: UserBody):
        return await super().create_one(data)
    
    @transaction
    async def update_one(self, id: Union[int, uuid.UUID], data: UserBody):
        return await super().update_one(id, data)
    
    @transaction
    async def delete_one(self, id: Union[int, uuid.UUID]):
        return await super().delete_one(id)
