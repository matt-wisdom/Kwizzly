import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEFAULT_TOKEN_EXPIRES: int = 15 * 86400  # 15 days
    DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://redis:6379/0"
    REDIS_HOST: str = (
        "localhost"  # "redis-11660.c258.us-east-1-4.ec2.cloud.redislabs.com"
    )
    REDIS_PORT: int = 6379
    MONGO_DATABASE_URI = "mongodb://db:27017"
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


#


class LocalConfig(Config):
    DB_URL: str = (
        ""
        if os.getenv("TESTING")
        else "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    )


class ProductionConfig(Config):
    DEBUG: str = False
    DB_URL: str = (
        ""
        if os.getenv("TESTING")
        else "mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"
    )


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
