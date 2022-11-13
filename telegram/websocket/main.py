import asyncio
import ssl
from asyncio.log import logger

from config import USE_SSL, WS_SERVER
from helper.redis import RedisBackend
from websockets.client import connect

from .quiz import play_game

redis = RedisBackend()


async def main():
    """
    Listen for new game request and create websocket session
    for each request.
    """
    pubsub = redis.subscribe("new_game_queue")
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    while True:
        try:
            msg = await pubsub.__anext__()
            if msg.get("type"):
                continue
            quiz_id = msg["quiz_id"]
            game_id = msg["game_id"]
            token = msg["token"]
            ws_server = WS_SERVER.format(token=token, quiz_id=quiz_id, game_id=game_id)
            if USE_SSL:
                ws = connect(ws_server, ssl=ssl_context)
            else:
                ws = connect(ws_server)
            asyncio.create_task(play_game(ws, game_id))
        except Exception as e:
            logger.exception(e)
        finally:
            await asyncio.sleep(0.5)


if __name__ == "__name__":
    asyncio.run(main())
