import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    DEFAULT_TOKEN_EXPIRES: int = 15 * 86400  # 15 days
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    REDIS_HOST: str = (
        "redis"
    )
    REDIS_PORT: int = 6379
    MONGO_DATABASE_URI = "mongodb://root:example@db:27017"
    MONGO_APP_DATABASE = "test_all" if os.getenv("TESTING") else "test_app"
    MONGO_USER_COLLECTION = "test_users"
    MONGO_TEXTS_COLLECTION = "test_texts"
    MONGO_QUIZ_COLLECTION = "test_quiz"
    MONGO_ATTEMPTS_COLLECTION = "test_attempts"
    MONGO_INVITES_COLLECTION = "test_invites"
    MONGO_GAMES_COLLECTION = "test_games"
    PER_PAGE = 8


class DevelopmentConfig(Config):
    MONGO_APP_DATABASE = "test_app" if os.getenv("TESTING") else "app"
    MONGO_USER_COLLECTION = "users"
    MONGO_TEXTS_COLLECTION = "texts"
    MONGO_QUIZ_COLLECTION = "quizes"
    MONGO_ATTEMPTS_COLLECTION = "attempts"
    MONGO_INVITES_COLLECTION = "invites"
    MONGO_GAMES_COLLECTION = "games"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG: str = False


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
