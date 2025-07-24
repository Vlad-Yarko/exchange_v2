import asyncio

# from backend.src.databases import sessionmanager
# from backend.src.models import Crypto, Currency


# uv run python -m backend.scripts.db


async def fill_crypto():
    pass


async def fill_currency():
    pass


async def main():
    tasks = asyncio.gather(
        fill_crypto(),
        fill_currency()
    )
    await tasks
    
    
asyncio.run(main())



# INSERT INTO users (username, password, email, phoneNumber, role, createdAt, updatedAt) VALUES 
# ("boba", "12345678zZ&", "boba@gmail.com", "+380888888888", "admin", NOW(), NOW())
