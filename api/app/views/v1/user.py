import pyotp
from app.schemas import ExceptionResponseSchema
from app.schemas.user import (
    ChangePasswordRequestSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserPaginatedSchema,
    GetUserResponseSchema,
    LoginResponseSchema,
    LoginUserRequestSchema,
)
from app.services import UserService
from core.exceptions.user import InvalidPasswordException, PasswordDoesNotMatchException
from core.fastapi.dependencies import IsAuthenticated, PermissionDependency
from core.utils import TokenHelper
from fastapi import APIRouter, Depends, HTTPException, Request

user_router = APIRouter()
otp_interval = 86400


@user_router.get(
    "/users",
    response_model=GetUserPaginatedSchema,
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_user_list(limit: int = -1, page: int = 1):
    return UserService().get_user_list(limit=limit, page=page)


@user_router.get(
    "/user/{user_id}",
    response_model=GetUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_user(user_id: str):
    return UserService().get_user(user_id)


@user_router.get(
    "/myprofile",
    response_model=GetUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_my(request: Request):
    return UserService().get_user(request.user.id)


@user_router.get(
    "/get_telegram_token",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_token(request: Request):
    """
    Get token for telegram registration
    """
    user = UserService().get_user(request.user.id, include_secret=True)
    print("user", user)
    token = pyotp.totp.TOTP(user.otp_secret, interval=otp_interval).now()
    return {"token": f"USER_{user.id}_" + token}


@user_router.get(
    "/redeem_token/{token}/{telegramid}",
    response_model=GetUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def redeem_token(request: Request, token: str, telegramid: str):
    """
    Redeem telegram token
    """
    _, user_id, token = token.split("_")
    user = UserService().get_user(user_id, include_secret=True)
    if not pyotp.totp.TOTP(user.otp_secret, interval=otp_interval).verify(token):
        raise HTTPException(400, "Invalid otp")
    _ = UserService().add_telegram(user.id, telegramid)
    return user


@user_router.get(
    "/get_auth_token_telegram/{telegram_id}",
    response_model=LoginResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_token_telegram(telegram_id: str):
    """
        Get auth token for telegram id
    """
    user = UserService().get_user_by_tg(telegram_id)
    access_token = TokenHelper.encode({"user_id": user.id}, 86400 / 2)
    return {**user.dict(), "access_token": access_token}


@user_router.post(
    "/register",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(request: CreateUserRequestSchema):
    """
        Register new user
    """
    user = UserService().create_user(**request.dict())
    access_token = TokenHelper.encode({"user_id": str(user.id)})
    return {**user.dict(), "access_token": access_token}


@user_router.post(
    "/login",
    response_model=LoginResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def login(request: LoginUserRequestSchema):
    """
        Login
    """
    is_success, user = UserService().check_password(
        email=request.email, password=request.password
    )
    if not is_success:
        raise InvalidPasswordException
    access_token = TokenHelper.encode({"user_id": str(user["_id"])})
    return {**user, "access_token": access_token}


@user_router.post(
    "/change-password",
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def change_password(request: ChangePasswordRequestSchema):
    """
        Change password
    """
    is_success, user = UserService().check_password(
        email=request.email, password=request.old_password
    )
    if not is_success:
        raise InvalidPasswordException
    if request.new_password != request.new_password2:
        raise PasswordDoesNotMatchException
    UserService().change_password(user.get("_id"), request.new_password)

    return {"message": "password changed"}

