import time
from typing import List

from app.schemas.quiz import (
    Attempt,
    CreateQuizSchema,
    GameSchema,
    GetAttemptsPaginatedSchema,
    GetGameSchema,
    GetQuizesPaginatedSchema,
    GetQuizSchema,
    InviteMultiplayerSchema,
    InviteNotificationSchema,
    InviteType,
    LaunchSchema,
)
from app.services.quiz import QuizService
from app.services.user import UserService
from core.db import attempts_db_client, games_db_client, invites_db_client
from core.fastapi.dependencies import IsAuthenticated, PermissionDependency
from core.helpers.cache import redis
from fastapi import APIRouter, Depends, Request

quiz_router = APIRouter()
quiz_per_page = 20


@quiz_router.post(
    "/create",
    response_model=GetQuizSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def create_quiz(request: CreateQuizSchema, req: Request):
    """
    Create quiz
    """
    quiz = QuizService().create_quiz(request, req)
    return quiz


@quiz_router.delete(
    "/{quiz_id}/delete",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def delete_quiz(quiz_id: str, req: Request):
    """
    Delete quiz
    """
    quiz = QuizService().delete_quiz(quiz_id, req)
    return quiz


@quiz_router.get(
    "/quiz/{quiz_id}",
    response_model=GetQuizSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def get_quiz(quiz_id: str, request: Request):
    """
    Retrieve quiz.
    """
    quiz = QuizService().get_quiz(quiz_id)
    if quiz.creator_id == request.user.id:
        quiz.is_creator = True
    return quiz


@quiz_router.get(
    "/{quiz_id}/leaderboard",
    response_model=GetAttemptsPaginatedSchema,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def quiz_leaderboard(quiz_id: str, page: int = 1):
    """
        Get leaderboad for single player games.
    """
    attempts_paginated = attempts_db_client.paginate_find(
        {"quiz_id": quiz_id}, per_page=None, page=page, sort="score"
    )
    attempts: List[Attempt] = attempts_paginated["data"]
    attempts.reverse()
    index = quiz_per_page * (page - 1)
    if len(attempts[index : index + quiz_per_page]) == quiz_per_page:
        attempts_paginated["has_next"] = True
    attempts_paginated["per_page"] = quiz_per_page
    attempts_paginated["data"] = attempts[index : index + quiz_per_page]
    return attempts_paginated


@quiz_router.get(
    "/quizes",
    response_model=GetQuizesPaginatedSchema,
)
async def get_quizes(limit: int = -1, page: int = 1):
    """
    Get all quizes
    """
    return QuizService().get_quizes(limit, page)


@quiz_router.get(
    "/{quiz_id}/launch-multiplayer",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def launch_multiplayer(quiz_id: str, request: Request):
    """
        Launch multiplayer game
    """
    user_id = request.user.id
    _ = UserService().get_user(user_id)
    _ = QuizService().get_quiz(quiz_id)
    game = GameSchema(timestamp=time.time(), creator_id=user_id, members=[user_id])
    game = games_db_client.insert(game.dict())
    return LaunchSchema(
        game_id=str(game.inserted_id),
        quiz_id=quiz_id,
        message="Game launched.",
        creator_id=user_id,
    )


@quiz_router.get(
    "/{quiz_id}/join",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def join_multiplayer(quiz_id: str, request: Request):
    """
    Join multiplayer game
    """
    user_id = request.user.id
    _ = UserService().get_user(user_id)
    _ = QuizService().get_quiz(quiz_id)
    game = GameSchema(timestamp=time.time(), creator_id=user_id, members=[user_id])
    game = games_db_client.insert(game.dict())
    return LaunchSchema(
        game_id=str(game.inserted_id),
        quiz_id=quiz_id,
        message="Joined Game.",
        creator_id=user_id,
    )


@quiz_router.get(
    "/game/{game_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    response_model=GetGameSchema,
)
async def get_game(game_id: str, request: Request):
    """
        Get game
    """
    user_id = request.user.id
    _ = UserService().get_user(user_id)
    game = QuizService().get_game(game_id)
    return game


@quiz_router.get(
    "/invite/{user_id}/{game_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def invite(user_id: str, game_id: str, game_url: str, request: Request):
    """
        Invite user to game
    """
    my_id = request.user.id
    my_user = UserService().get_user(my_id)
    invite = InviteMultiplayerSchema(target_id=user_id, game_id=game_id, url=game_url)
    _ = invites_db_client.insert(invite.dict())
    notify = InviteNotificationSchema(
        target_id=user_id,
        msg=f"{my_user.nickname} wants to play a game now. Click to participate.",
        type=InviteType.multiplayer,
        game_id=game_id,
        url=game_url,
    )
    invite = invites_db_client.insert(invite.dict())
    await redis.publish(user_id, notify.dict())
    return {"message": "invited "}


@quiz_router.get(
    "/invite-again/{game_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
async def invite_again(game_id: str, game_url: str, request: Request):
    """
        Invite user for a rematch
    """
    my_id = request.user.id
    my_user = UserService().get_user(my_id)
    game = QuizService().get_game(game_id)
    for user_id in game.members:
        if user_id == my_id:
            continue
        invite = InviteMultiplayerSchema(
            target_id=user_id, game_id=game_id, url=game_url
        )
        _ = invites_db_client.insert(invite.dict())
        notify = InviteNotificationSchema(
            target_id=user_id,
            msg=f"{my_user.nickname} wants to play a game now. Click to participate.",
            type=InviteType.multiplayer,
            game_id=game_id,
            url=game_url,
        )
        invite = invites_db_client.insert(invite.dict())
        await redis.publish(user_id, notify.dict())
    return {"message": "invited "}
