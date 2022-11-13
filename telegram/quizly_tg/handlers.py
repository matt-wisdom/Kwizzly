from asyncio.log import logger

from config import API_BACKEND, FRONTEND_BASE_URL
from helper.redis import RedisBackend
from telethon import TelegramClient, events

from . import messages
from .api import QuizlyAPI
from .database import User, session
from .error_handlers import catch_errors
from .game import join_game, play_multi_player
from .utils import send_with_action, validate_token

api_client = QuizlyAPI(API_BACKEND)
redis = RedisBackend()


@catch_errors()
async def start_handler(event: events.NewMessage.Event, bot: TelegramClient):
    """
    First time users should first send the /start command.
    A user account will be created for them.

    NOTE: The first person to connect to the bot becomes the admin
    """
    sender_tg = await event.get_sender()
    sender_id = event.sender_id

    async with bot.conversation(await event.get_chat(), exclusive=False) as conv:
        await conv.cancel_all()
        # await event.respond("Conversations cancelled.")

    sender = User.query.filter_by(user_id=sender_id).first()
    if not sender:
        sender = User(user_id=sender_id, username=sender_tg.username)
        session.add(sender)
        session.commit()
        await event.respond(messages.welcome_new)
        await event.respond(messages.register_token.format(url=FRONTEND_BASE_URL))
    else:
        await event.respond(messages.welcome_old)
    await send_with_action(sender, messages.registered, bot)

    raise events.StopPropagation


@catch_errors()
async def new_message_handler(event: events.NewMessage.Event, bot: TelegramClient):
    try:
        data = event.text
        sender_id = event.sender_id
        sender: User = User.query.filter_by(user_id=sender_id).first()
        if not sender:
            await bot.send_message(sender_id, messages.not_registered)
        if data == messages.input_token:
            await validate_token(bot, sender_id, api_client)
        elif data == messages.join_game_action:
            await join_game(bot, sender_id, api_client)
        elif data == messages.help:
            # Help
            await send_with_action(sender, messages.help_msg.format(admin=""), bot)
        elif data == messages.play_multiplayer:
            await play_multi_player(bot, sender_id, sender, api_client)
        else:
            pass
            # await send_with_action(sender, messages.invalid, bot)
    except Exception as e:
        logger.exception(e)
        session.rollback()


@catch_errors()
async def callback_handler(event: events.NewMessage.Event, bot: TelegramClient):
    """
    Callbacks for inline buttons
    """
    pass
