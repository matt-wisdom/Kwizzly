import os

import aioredis
from core.config import config

redis = aioredis.from_url(
    url=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
    username=os.getenv("REDIS_USER"),
    password=os.getenv("REDIS_PASS"),
)
