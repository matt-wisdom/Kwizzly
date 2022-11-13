from asyncio.log import logger
from typing import List

from quizly_tg.api import QuizlyAPI
from telethon import TelegramClient
from telethon.tl.custom import Button, Conversation

from . import messages
from .database import User
from .error_handlers import catch_errors


def get_action_buttons(sender: User) -> List[List[Button]]:
    """
    Get buttons for main bot actions

    :param sender: sender's data
    """
    registered_buttons = [
        [Button.text(messages.input_token), Button.text(messages.play_multiplayer)],
        [Button.text(messages.join_game_action), Button.text(messages.help)],
    ]
    return registered_buttons


@catch_errors()
async def send_with_action(sender: User, message: str, bot: TelegramClient):
    """
    Send a message with buttons for main bot actions.

    :param sender: sender's data
    :param message: message to send
    :param bot: telethon's TelegramClient for the bot
    """

    registered_buttons = get_action_buttons(sender)
    markup = bot.build_reply_markup(registered_buttons)
    await bot.send_message(sender.user_id, message, buttons=markup)


@catch_errors()
async def get_resp_msg(conv: Conversation, msg: str) -> str:
    """
    :param conv: Telethon Conversation object
    :param msg: str
    """
    await conv.send_message(msg)
    response = await conv.get_response()
    return response.text


async def validate_token(bot: TelegramClient, sender_id: str, api_client: QuizlyAPI):
    """
    Receive and validate token

    :param bot: Telethon Client object
    :param sender_id: sender id
    :param api_client: API client

    """
    async with bot.conversation(sender_id, exclusive=False) as conv:
        token = await get_resp_msg(conv, messages.get_token)
        try:
            await api_client.register_token(token, sender_id)
            await conv.send_message(messages.registered_token)
        except Exception as e:
            logger.exception(e)
            await conv.send_message(str(e))
