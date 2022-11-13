import asyncio
from asyncio.log import logger

import dotenv

# from quizly_tg.database import create_all
from quizly_tg.bot import create_bot
from quizly_tg.database import session

dotenv.load_dotenv(dotenv.find_dotenv())


async def main():
    try:
        bot = await create_bot()
        await bot.run_until_disconnected()

        await asyncio.sleep(5)
    except Exception as e:
        logger.exception(e)
        session.rollback()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
