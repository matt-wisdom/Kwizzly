import json
import pickle
from typing import Any, AsyncGenerator

import ujson
from core.helpers.cache.base import BaseBackend
from core.helpers.redis import redis


class RedisBackend(BaseBackend):
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
