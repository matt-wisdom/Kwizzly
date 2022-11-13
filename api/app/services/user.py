from typing import NoReturn, Optional, Tuple, Union

import pyotp
from app.schemas.user import (
    GetUserPaginatedSchema,
    GetUserResponseSchema,
    GetUserResponseWithSecretSchema,
)
from bson.objectid import ObjectId
from core.db import user_db_client
from core.exceptions import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserDoesNotExist,
)
from pymongo.results import UpdateResult
from werkzeug.security import check_password_hash, generate_password_hash


class UserService:
    def __init__(self):
        pass

    def get_user(
        self, user_id: str, include_secret=False
    ) -> Union[GetUserResponseSchema, GetUserResponseWithSecretSchema]:
        user = user_db_client.find({"_id": ObjectId(user_id)})
        if not user:
            raise UserDoesNotExist
        if include_secret:
            return GetUserResponseWithSecretSchema(**user[0])
        return GetUserResponseSchema(**user[0])

    def get_user_by_tg(self, tg_id: str) -> GetUserResponseSchema:
        user = user_db_client.find({"telegramid": tg_id})
        if not user:
            raise UserDoesNotExist
        return GetUserResponseSchema(**user[0])

    def add_telegram(self, user_id: str, telegramid: str) -> UpdateResult:
        return user_db_client.update(
            {"_id": ObjectId(user_id)}, {"$set": {"telegramid": telegramid}}
        )

    def get_user_email(self, email: str) -> GetUserResponseSchema:
        user = user_db_client.paginate_find({"email": email})
        return GetUserResponseSchema(**user[0])

    def get_user_list(
        self,
        limit: Optional[int] = -1,
        page: Optional[int] = None,
    ) -> GetUserPaginatedSchema:
        if not page:
            page = 1
        users = user_db_client.paginate_find({}, page, limit)
        return GetUserPaginatedSchema(**users)

    def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> Union[GetUserResponseSchema, NoReturn]:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        is_exist = user_db_client.find({"email": email})
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = user_db_client.insert(
            {
                "email": email,
                "password": generate_password_hash(password1),
                "nickname": nickname,
                "is_admin": False,
                "otp_secret": pyotp.random_base32(),
            }
        )

        return GetUserResponseSchema(**self.get_user(user.inserted_id).dict())

    def change_password(self, user_id: str, new_password):
        user_db_client.update(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": generate_password_hash(new_password)}},
        )

    def check_password(
        self, email: str, password: str
    ) -> Tuple[bool, GetUserResponseSchema]:
        user = user_db_client.find({"email": email})
        if not user:
            raise UserDoesNotExist
        user = user[0]
        return check_password_hash(user["password"], password), user

    def is_admin(self, user_id: str) -> bool:
        result = user_db_client.find({"_id": ObjectId(user_id)})
        if not result:
            raise UserDoesNotExist

        if result[0].is_admin is False:
            return False

        return True
