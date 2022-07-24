from typing import Optional, List, Union, NoReturn

from bson.objectid import ObjectId
from app.schemas import (
    GetUserResponseSchema,
    GetUserPaginatedSchema,
    CreateUserRequestSchema
)
from core.db import user_db_client
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserDoesNotExist
)


class UserService:
    def __init__(self):
        pass
    
    async def get_user(
        self,
        user_id: str
    ) -> GetUserResponseSchema:
        user = user_db_client.paginate_find(
                {"_id": ObjectId(user_id)})
        return user[0]

    async def get_user_list(
        self,
        limit: Optional[int] = -1,
        page: Optional[int] = None,
    ) -> GetUserPaginatedSchema:
        if not page:
            page = 1
        users = user_db_client.paginate_find({}, page, limit)
        return users

    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> Union[GetUserResponseSchema, NoReturn]:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        is_exist = user_db_client.find({"email": email})
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = user_db_client.insert({"email": email,
            "password": password1, "nickname": nickname,
            "is_admin": False})

        return user

    async def is_admin(self, user_id: str) -> bool:
        result = user_db_client.find({"_id": ObjectId(user_id)})
        if not result:
            raise UserDoesNotExist

        if result[0].is_admin is False:
            return False

        return True
