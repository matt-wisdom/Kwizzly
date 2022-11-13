from typing import Optional

import jwt
from app.services.user import UserService
from core.helpers.cache import redis
from core.utils.token_helper import TokenHelper
from fastapi import Depends, Query, WebSocket, status


async def check_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    # print(token)
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    try:
        payload = TokenHelper.decode(token)
        user_id = payload.get("user_id")
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return user_id


async def notifications(websocket: WebSocket, user_id: str = Depends(check_token)):
    await websocket.accept()
    _ = UserService().get_user(user_id)
    async for msg in redis.subscribe(user_id):
        print("MSG", msg)
        if msg["type"] == "subscribe":
            continue
        await websocket.send_json(msg)
