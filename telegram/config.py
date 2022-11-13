DB_ENGINE = "sqlite:///dev.db?check_same_thread=False"
REDIS_HOST = "redis"
REDIS_PORT = 6379  # 11660
WS_SERVER = "ws://api:8080/game/multiplayer?token={token}&quiz_id={quiz_id}&game_id={game_id}"
USE_SSL = False
API_BACKEND = "http://redis:8000/api"
FRONTEND_BASE_URL = "http://localhost:9999/"
