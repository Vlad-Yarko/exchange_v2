import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.mysql_manager import db_session
from src.models import Crypto, Currency
from src.constants.crypto import CRYPTO_SYMBOLS
from src.constants.currency import CURRENCY_SYMBOLS


# python -m scripts.db.data


async def fill_crypto(session: AsyncSession):
    symbols = [
        Crypto(symbol=f"{name}USDT", symbol1=name, symbol2="USDT")
        for name in CRYPTO_SYMBOLS
    ]
    session.add_all(symbols)


async def fill_currency(session: AsyncSession):
    symbols = []
    for i in range(len(CURRENCY_SYMBOLS)):
        symbol1 = CURRENCY_SYMBOLS[i]
        for j in range(len(CURRENCY_SYMBOLS)):
            symbol2 = CURRENCY_SYMBOLS[j]
            if symbol1 != symbol2:
                symbols.append(Currency(symbol=f"{symbol1}{symbol2}", symbol1=symbol1, symbol2=symbol2))
    session.add_all(symbols)


async def main():
    async for session in db_session():
        tasks = asyncio.gather(
            fill_crypto(session),
            fill_currency(session)
        )
        await tasks
        await session.commit()
    
    
asyncio.run(main())
