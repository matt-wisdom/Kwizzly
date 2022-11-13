import logging

from config import DB_ENGINE
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Query, sessionmaker

Base = declarative_base()
engine = create_engine(DB_ENGINE)
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
Session = sessionmaker(bind=engine)
session = Session()


def create_all():
    Base.metadata.create_all(engine)


class BaseModel:
    @classmethod
    @hybrid_property
    def query(cls) -> Query:
        return session.query(cls)


class User(BaseModel, Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)  # Telegram user_id
    username = Column(String)  # Username or name

    def __repr__(self) -> str:
        return f"User: {self.user_name} - ID: {self.id}"
