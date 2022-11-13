from bson import ObjectId
from pydantic import BaseModel


class ExceptionResponseSchema(BaseModel):
    error: str


class BSONObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("ObjectId reqiured")
        return str(v)
