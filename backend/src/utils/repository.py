from abc import ABC, abstractmethod
from typing import Union, Optional
import uuid
from functools import wraps

from sqlalchemy import func, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base
from src.utils.logger import logger


class Repository(ABC):
    
    @abstractmethod
    async def get():
        raise NotImplementedError
    
    @abstractmethod
    async def get_one():
        raise NotImplementedError
    
    @abstractmethod
    async def get_count():
        raise NotImplementedError
    
    @abstractmethod
    async def create_one():
        raise NotImplementedError
    
    @abstractmethod
    async def update_one():
        raise NotImplementedError
    
    @abstractmethod
    async def delete_one():
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
        return conditions
        
    async def get_count(self, **kwargs) -> Optional[int]:
        conditions = self.equal_conditions(**kwargs)
        query = select(func.count()).select_from(self.model).where(*conditions)
        data = await self.session.execute(query)
        data = data.scalar_one()
        return data
    
    async def get(self, page: Optional[int] = None, **kwargs) -> Optional[tuple[list[Base], int, int]]:
        conditions = self.equal_conditions(**kwargs)
        query = None
        total = await self.get_count(**kwargs)
        if page is None:
            query = select(self.model).where(*conditions)
        else:
            offset_page = page - 1
            offset = self.PAGINATION_OFFSET * offset_page
            query = select(self.model).where(*conditions).offset(offset).limit(self.PAGINATION_LIMIT)
        data = await self.session.execute(query)
        data = data.scalars().all()
        return data, total, self.PAGINATION_OFFSET
        
    
    async def get_one(self, **kwargs) -> Optional[Base]:
        conditions = [getattr(self.model, field_name) == value for field_name, value in kwargs.items()]
        query = select(self.model).where(*conditions)
        data = await self.session.execute(query)
        obj = data.scalar()
        return obj
    
    async def get_one_by_id(self, id: Union[int, uuid.UUID]) -> Optional[Base]:
        return await self.get_one(id=id)
    
    async def get_latest(self, **kwargs) -> Optional[list[Base]]:
        conditions = self.equal_conditions(**kwargs)
        query = select(self.model).where(*conditions).order_by(self.model.createdAt.desc()).limit(self.LATEST_LIMIT)
        data = await self.session.execute(query)
        return data.scalars().all()
    
    async def create_one(self, **kwargs) -> Optional[Base]:
        # PostgreSQL has RETURNING
        # stmt = insert(self.model).values(**kwargs).returning(self.model)
        # obj = await self.session.execute(stmt)
        # return obj.scalar()
        # MySQL
        stmt = insert(self.model).values(**kwargs)
        result = await self.session.execute(stmt)
        obj = await self.get_one_by_id(result.lastrowid)
        return obj
    
    async def update_one(self, id: Union[int, uuid.UUID], **kwargs) -> Optional[Base]:
        # PostgreSQL has RETURNING
        # smtp = update(self.model).where(self.model.id == id).values(**kwargs).returning(self.model)
        # obj = await self.session.execute(smtp)
        # return obj.scalar()
        # MySQL
        smtp = update(self.model).where(self.model.id == id).values(**kwargs)
        await self.session.execute(smtp)
        obj = await self.get_one_by_id(id)
        return obj
    
    async def delete_one(self, id: Union[int, uuid.UUID]) -> Optional[Base]:
        # PostgreSQL has RETURNING
        # smtp = delete(self.model).where(self.model.id == id).returning(self.model)
        # obj = await self.session.execute(smtp)
        # return obj.scalar()
        # MySQL
        obj = await self.get_one_by_id(id)
        smtp = delete(self.model).where(self.model.id == id)
        await self.session.execute(smtp)
        return obj


def transaction(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        result = None
        rollback_needed = False
        try:
            result = await func(self, *args, **kwargs)
            if isinstance(result, tuple):
                rollback_needed = True
            return result
        except Exception as e:
            await self.session.rollback()
            logger.critical("DATABASE ERROR")
            logger.critical(str(e))
            raise ValueError("DATABASE ERROR")
        finally:
            if rollback_needed:
                await self.session.rollback()
            else:
                await self.session.commit()
    return wrapper
