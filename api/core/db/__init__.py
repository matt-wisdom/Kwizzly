from core.config import config
from core.db.db import MongoDBClient

user_db_client = MongoDBClient(config.MONGO_APP_DATABASE, config.MONGO_USER_COLLECTION)
quiz_db_client = MongoDBClient(config.MONGO_APP_DATABASE, config.MONGO_QUIZ_COLLECTION)
texts_db_client = MongoDBClient(
    config.MONGO_APP_DATABASE, config.MONGO_TEXTS_COLLECTION
)
attempts_db_client = MongoDBClient(
    config.MONGO_APP_DATABASE, config.MONGO_ATTEMPTS_COLLECTION
)
invites_db_client = MongoDBClient(
    config.MONGO_APP_DATABASE, config.MONGO_INVITES_COLLECTION
)
games_db_client = MongoDBClient(
    config.MONGO_APP_DATABASE, config.MONGO_GAMES_COLLECTION
)

__all__ = ["MongoDBClient"]
