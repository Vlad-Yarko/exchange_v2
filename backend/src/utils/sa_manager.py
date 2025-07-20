from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)

from src.utils.db_manager import DatabaseManager


class SQLAlchemyManager(DatabaseManager):
    SQLALCHEMY_DATABASE_URL = None

    def __init__(self):
        self.__engine: AsyncEngine | None = None
        self.__session_fabric: async_sessionmaker | None = None

    def connect_to_db(self):
        self.__engine = create_async_engine(self.SQLALCHEMY_DATABASE_URL)
        self.__session_fabric = async_sessionmaker(autocommit=False, bind=self.__engine)

    async def close(self):
        if self.__engine is None:
            raise Exception("Engine wasn't initialized")

        await self.__engine.dispose()
        self.__engine = None
        self.__session_fabric = None

    @asynccontextmanager
    async def sessions(self):
        if self.__session_fabric is None:
            raise Exception("sessionmaker is not initialized")

        session = self.__session_fabric()

        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
