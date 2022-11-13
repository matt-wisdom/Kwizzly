from urllib.parse import urlencode

import httpx


class QuizlyAPI:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.strip("/")
        self.client = httpx.AsyncClient()

    async def _get(self, endpoint: str, **kwargs) -> httpx.Response:
        token = kwargs.get("token")
        if token:
            token = kwargs.pop("token")
            bearer = f"Bearer {token}"
            if not kwargs.get("headers"):
                kwargs["headers"] = {}
            kwargs["headers"]["Authorization"] = bearer
        resp = await self.client.get(f"{self.base_url}{endpoint}", **kwargs)
        if resp.is_error:
            resp.raise_for_status()
        return resp

    async def _post(self, endpoint: str, **kwargs) -> httpx.Response:
        token = kwargs.get("token")
        if token:
            token = kwargs.pop("token")
            bearer = f"Bearer {token}"
            if not kwargs.get("headers"):
                kwargs["headers"] = {}
            kwargs["headers"]["Authorization"] = bearer
        resp = await self.client.post(f"{self.base_url}{endpoint}", **kwargs)
        if resp.is_error:
            resp.raise_for_status()
        return resp

    async def _close(self) -> None:
        await self.client.aclose()

    async def register_token(self, token: str, telegramid: str) -> None:
        await self._get(f"/users/redeem_token/{token}/{telegramid}")

    async def get_auth_token(self, telegramid: str) -> dict:
        res = await self._get(f"/users/get_auth_token_telegram/{telegramid}")
        return res.json()

    async def launch_multiplayer(
        self, quiz_id: str, origin: str, auth_token: str, again: str = None
    ):
        resp = await self._get(f"/quiz/{quiz_id}/launch-multiplayer", token=auth_token)
        data = resp.json()
        game_id = data["game_id"]
        join_url = f"{origin}/join-multi/{game_id}?quiz_id={quiz_id}"
        if again:
            _ = await self._get(
                f"/quiz/invite-again/{again}?game_url={urlencode(join_url)}",
                token=auth_token,
            )
        return join_url, game_id
