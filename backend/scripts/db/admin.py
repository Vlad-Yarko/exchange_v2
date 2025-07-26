import asyncio

from sqlalchemy import insert

from src.databases.mysql_manager import db_session
from src.models import User
from src.utils.password import pw_manager


# python -m scripts.db.admin


async def main():
    async for session in db_session():
        await session.execute(insert(User).values(
            username="boba",
            password=pw_manager.hash_password("12345678zZ&"),
            email="boba@gmail.com",
            role="ADMIN"
        ))
        await session.commit()


if __name__ == '__main__':
    asyncio.run(main())
