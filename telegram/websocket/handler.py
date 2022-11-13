import json

from websockets.client import WebSocketClientProtocol

from . import redis


async def handle_server_msg(data: dict, game_id: str):
    """
    Handler for server messages from redis pusub
    """
    type = data["type"]
    print("got server", type)
    pubsub = f"telegram_{game_id}_server_msg"

    async def publish(type, data):
        await redis.publish(pubsub, {"type": type, "data": data})

    async def send_data(type, data):
        await publish(type=type, data=data)

    if type == "timeout":
        pass
    elif type == "register":
        pass
    elif type == "ended":
        await publish(type="message", data="Can't join. Game already played")
    elif type == "no_participant":
        await publish(type="message", data="No participants")
        return False
    elif type == "already_started":
        await publish(type="message", data="Can't join. Game already started")
        return False
    elif type == "started":
        await publish(type="started", data="Game started")
    elif type == "start":
        await publish(type="start", data="")
    elif type == "finished":
        print("Finshed", data)
        await publish(type="finished", data=data["data"])
        return False
    else:
        await send_data(type, data)


async def handle_user_action(data: dict, ws: WebSocketClientProtocol):
    """
    Handler for messages from telegram user
    """
    type = data["type"]
    print("Got action", type, data)
    if type == "my_answer":
        await ws.send(json.dumps(data))
    elif type == "close":
        return False
