from typing import List, Optional

from pydantic import BaseModel, EmailStr


class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: str


class ChangePasswordRequestSchema(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str
    new_password2: str


class ChangeEmailRequestSchema(BaseModel):
    email: EmailStr
    new_email: EmailStr
    password: str


class GetUserResponseSchema(BaseModel):
    id: str
    email: EmailStr
    nickname: str
    telegramid: Optional[int]


class GetUserResponseWithSecretSchema(BaseModel):
    id: str
    email: EmailStr
    nickname: str
    telegramid: Optional[int]
    otp_secret: str


class LoginResponseSchema(BaseModel):
    id: str
    email: EmailStr
    nickname: str
    telegramid: Optional[int]
    access_token: str


class GetUserPaginatedSchema(BaseModel):
    per_page: int
    page: int
    data: List[GetUserResponseSchema]
    has_next: bool


class CreateUserRequestSchema(BaseModel):
    email: EmailStr
    password1: str
    password2: str
    nickname: str


class CreateUserResponseSchema(BaseModel):
    id: str
    email: EmailStr
    nickname: str
    access_token: str
