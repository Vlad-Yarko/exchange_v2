from src.utils.sa_manager import SQLAlchemyManager
from src.config import settings


class MySQLManager(SQLAlchemyManager):
    SQLALCHEMY_DATABASE_URL = settings.MYSQL if settings.TEST_ENVIRONMENT == "false" else settings.TEST_MYSQL
    
    
sessionmanager = MySQLManager()


async def get_db_session():
    async with sessionmanager.sessions() as session:
        yield session
        
        
async def db_session():
    sessionmanager.connect_to_db()
    async with sessionmanager.sessions() as session:
        yield session
