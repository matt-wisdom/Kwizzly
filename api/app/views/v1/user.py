from typing import List

from fastapi import APIRouter, Depends

from app.schemas import (
    ExceptionResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserPaginatedSchema
)
from app.services import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)

user_router = APIRouter()


@user_router.get(
    "/users",
    response_model=GetUserPaginatedSchema,
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(limit: int = -1, page: int = 1):
    return await UserService().get_user_list(limit=limit, page=page)


@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(request: CreateUserRequestSchema):
    return await UserService().create_user(**request.dict())


