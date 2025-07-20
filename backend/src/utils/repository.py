from abc import ABC, abstractmethod
from typing import Union, Optional
import uuid
from functools import wraps

from sqlalchemy import insert, select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


class Repository(ABC):
    @abstractmethod
    async def create_one():
        raise NotImplementedError
    
    @abstractmethod
    async def select_one():
        raise NotImplementedError
    
    @abstractmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractmethod
    async def select_all():
        raise NotImplementedError
    
    @abstractmethod
    async def select_count():
        raise NotImplementedError
    
    
class SQLAlchemyRepository(Repository):
    model = None
    PAGINATION_OFFSET = 15
    PAGINATION_LIMIT = 15
    LATEST_LIMIT = 10
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    def equal_conditions(self, **kwargs) -> list:
        conditions = []
        for key, value in kwargs.items():
            if value:
                condition = getattr(self.model, key) == value
                conditions.append(condition)
        # conditions = [
        #     getattr(self.model, key) == value
        #     for key, value in kwargs.items()
        # ]
        return conditions
        
    async def select_count(self, **kwargs) -> Optional[int]:
        conditions = self.equal_conditions(**kwargs)
        query = select(func.count()).select_from(self.model).where(*conditions)
        data = await self.session.execute(query)
        data = data.scalar_one()
        return data
    
    async def select_all(self, page: Optional[int] = None, **kwargs) -> Optional[tuple[list[Base], int, int]]:
        conditions = self.equal_conditions(**kwargs)
        query = None
        total = await self.select_count(**kwargs)
        if page is None:
            query = select(self.model).where(*conditions)
        else:
            offset_page = page - 1
            offset = self.PAGINATION_OFFSET * offset_page
            query = select(self.model).where(*conditions).offset(offset).limit(self.PAGINATION_LIMIT)
        data = await self.session.execute(query)
        data = data.scalars().all()
        return data, total, self.PAGINATION_OFFSET
        
    
    async def select_one(self, field_name: str, value: Union[int, str, uuid.UUID]) -> Optional[Base]:
        query = select(self.model).where(getattr(self.model, field_name) == value)
        data = await self.session.execute(query)
        obj = data.scalar()
        return obj
    
    async def select_one_by_id(self, id: Union[int, uuid.UUID]) -> Optional[Base]:
        return await self.select_one("id", id)
    
    async def select_latest(self, **kwargs) -> Optional[list[Base]]:
        conditions = self.equal_conditions(**kwargs)
        query = select(self.model).where(*conditions).order_by(self.model.createdAt.desc()).limit(self.LATEST_LIMIT)
        data = await self.session.execute(query)
        return data.scalars().all()
    
    async def create_one(self, **kwargs) -> Union[int, uuid.UUID]:
        stmt = insert(self.model).values(**kwargs).returning(self.model.id)
        id = await self.session.execute(stmt)
        return id.scalar()
    
    async def update_one(self, id: Union[int, uuid.UUID], **kwargs) -> Union[int, uuid.UUID]:
        # print("KKKKK", kwargs)
        smtp = update(self.model).where(self.model.id == id).values(**kwargs).returning(self.model.id)
        id = await self.session.execute(smtp)
        await self.session.commit()
        return id.scalar()


def transaction(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception:
            await self.session.rollback()
            raise
        finally:
            await self.session.commit()
    return wrapper
