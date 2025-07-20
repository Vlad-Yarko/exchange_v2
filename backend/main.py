import asyncio

from src import API, Bot


api = API()
api.create()

bot = Bot()
bot.create()


async def main():
    await asyncio.gather(
        api.run(),
        bot.run()
    )


if __name__ == "__main__":
    pass
