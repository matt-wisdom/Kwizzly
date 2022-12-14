import asyncio
import logging
import os
from typing import Tuple

import dotenv
from telethon import TelegramClient, events

from .handlers import callback_handler, new_message_handler, start_handler

# from .database import User

dotenv.load_dotenv(dotenv.find_dotenv())

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


async def create_bot() -> Tuple[TelegramClient, asyncio.Task]:
    """
    Create bot and register handlers
    """
    bot = await TelegramClient("bot", os.getenv("API_ID"), os.getenv("API_HASH")).start(
        bot_token=os.getenv("BOT_TOKEN")
    )
    await register_handlers(bot)

    return bot


async def register_handlers(bot: TelegramClient) -> None:
    """
    Register handlers for events.
    """

    @bot.on(events.NewMessage)
    async def message(event):
        await new_message_handler(event, bot)

    @bot.on(events.NewMessage(pattern="/start"))
    async def start(event):
        await start_handler(event, bot)

    @bot.on(events.CallbackQuery)
    async def callback(event):
        await callback_handler(event, bot)
