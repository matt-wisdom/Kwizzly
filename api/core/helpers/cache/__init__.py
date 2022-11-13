import asyncio
from contextlib import asynccontextmanager

from core.helpers.cache.redis_backend import RedisBackend

from .cacheable import Cacheable

redis = RedisBackend()


@asynccontextmanager
async def redis_lock(game_id: str):
    """
    Lock for accessing redis game resources concurrently
    """
    while int((await redis.get(game_id))["lock"]):
        await asyncio.sleep(0.5)
    try:
        scores_data = await redis.get(game_id)
        scores_data["lock"] = 1
        await redis.save(scores_data, game_id)
        yield
    finally:
        scores_data = await redis.get(game_id)
        scores_data["lock"] = 0
        await redis.save(scores_data, game_id)


__all__ = [
    "Cacheable",
]
