import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = None
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    MONGO_DATABASE_URI = "mongodb://127.0.0.1:27017"
    MONGO_APP_DATABASE = "test_app"
    MONGO_USER_COLLECTION = "test_users"
    MONGO_TEXTS_COLLECTION = "test_texts"
    MONGO_QUESTIONS_COLLECTION = "test_questions"
    PER_PAGE = 15


class DevelopmentConfig(Config):
    DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"
    MONGO_APP_DATABASE = "app"
    MONGO_USER_COLLECTION = "users"
    MONGO_TEXTS_COLLECTION = "texts"
    MONGO_QUESTIONS_COLLECTION = "questions"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"


class ProductionConfig(Config):
    DEBUG: str = False
    DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "development": DevelopmentConfig(),
        "local": LocalConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
