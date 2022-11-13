import json
import os
import pickle
from typing import Any, AsyncGenerator

import aioredis
import config
import dotenv
import ujson

dotenv.load_dotenv(".env")

redis = aioredis.from_url(url=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}")


class RedisBackend:
    async def get(self, key: str) -> Any:
        result = await redis.get(key)
        if not result:
            return

        try:
            return ujson.loads(result.decode("utf8"))
        except UnicodeDecodeError:
            return pickle.loads(result)

    async def save(self, response: Any, key: str, ttl: int = 3600) -> None:
        if isinstance(response, dict):
            response = ujson.dumps(response)
        elif isinstance(response, object):
            response = pickle.dumps(response)

        await redis.set(name=key, value=response, ex=ttl)

    async def subscribe(self, channel: str) -> AsyncGenerator:
        sub = redis.pubsub()
        await sub.subscribe(channel)

        async for message in sub.listen():
            if message["type"] == "message":
                message = json.loads(message["data"])
            if message is not None and isinstance(message, dict):
                yield message

    async def publish(self, channel: str, message: dict) -> int:
        message = json.dumps(message)
        return await redis.publish(channel, message)
