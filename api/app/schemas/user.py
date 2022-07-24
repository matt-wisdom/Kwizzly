from typing import List, Optional
from pydantic import BaseModel


class GetUserResponseSchema(BaseModel):
    id: int
    email: str
    nickname: str
    telegram_id: Optional[int]

class GetUserPaginatedSchema(BaseModel):
    per_page: int
    page: int
    data: List[GetUserResponseSchema]
    has_next: bool

class CreateUserRequestSchema(BaseModel):
    email: str
    password1: str
    password2: str
    nickname: str


class CreateUserResponseSchema(BaseModel):
    id: int
    email: str
    nickname: str

    class Config:
        orm_mode = True
