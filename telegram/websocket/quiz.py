import asyncio
import json

from websockets.client import WebSocketClientProtocol

from . import redis
from .handler import handle_server_msg, handle_user_action


# websockets.connect()
async def get_user_action(game_id: str, redis_queue: asyncio.Queue):
    """
    Get data from redis pubsub
    """
    other_answers = redis.subscribe(f"telegram_{game_id}_actions")
    while True:
        data = await other_answers.__anext__()
        await redis_queue.put(["user", data])
        await asyncio.sleep(0.05)


async def get_server_msg(ws: WebSocketClientProtocol, ws_queue: asyncio.Queue):
    """
    Get data from websocket server
    """
    while True:
        data = json.loads(await ws.recv())
        await ws_queue.put(["ws", data])
        await asyncio.sleep(0.05)


async def play_game(wsock: WebSocketClientProtocol, game_id: str):
    """
    Manage gameplay.
    Recieve user actions and send responses.
    """
    await asyncio.sleep(14)
    async with wsock as ws:

        async def send_start():
            # Useless if not creator
            await asyncio.sleep(5)
            await ws.send(json.dumps({"type": "start"}))

        asyncio.create_task(send_start())
        try:
            queue = asyncio.Queue(1000)
            game_pubsub = asyncio.create_task(get_user_action(game_id, queue))
            ws_task = asyncio.create_task(get_server_msg(ws, queue))
            while True:
                await asyncio.sleep(0.05)
                try:
                    res = queue.get_nowait()
                except asyncio.QueueEmpty:
                    continue
                if res[0] == "ws":
                    _ = await handle_server_msg(res[1], game_id)
                elif res[0] == "user":
                    _ = await handle_user_action(res[1], ws)
                else:
                    raise ValueError("Invalid type")
                # if not unfinished:
                #     return
        except Exception as e:
            print(e)
        finally:
            await ws.close()
            game_pubsub.cancel()
            ws_task.cancel()
