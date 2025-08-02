import asyncio

from src import api, bot


async def main():
    await asyncio.gather(
        bot.run(),
        api.run()
    )


if __name__ == "__main__":
    asyncio.run(main())
