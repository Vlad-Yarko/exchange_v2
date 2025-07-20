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
