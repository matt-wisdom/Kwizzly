from core.db.db import MongoDBClient
from core.config import config

user_db_client = MongoDBClient(config.MONGO_APP_DATABASE, config.MONGO_USER_COLLECTION)
question_db_client = MongoDBClient(config.MONGO_APP_DATABASE, config.MONGO_QUESTIONS_COLLECTION)
texts_db_client = MongoDBClient(config.MONGO_APP_DATABASE, config.MONGO_TEXTS_COLLECTION)

__all__ = [
    "MongoDBClient"
]
