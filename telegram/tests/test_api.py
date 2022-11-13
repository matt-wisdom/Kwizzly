from dataclasses import dataclass
from typing import List

import pytest
from quizly_tg.api import QuizlyAPI


@dataclass
class MockResp:
    is_error: bool = False

    def json(self):
        return {}


@dataclass
class MockClient:
    url_contains: List[str]
    kwargs_props: dict = None

    async def get(self, url, **kwargs):
        for i in self.url_contains:
            assert i in url
        if self.kwargs_props:
            for key, value in self.kwargs_props.items():
                assert kwargs.get(key) == value
        return MockResp()

    async def post(self, url, **kwargs):
        return await self.get(url, **kwargs)


@pytest.mark.asyncio
async def test_get_post():
    api_client = QuizlyAPI("http://127.0.0.1")
    tok = "Defgtg"
    endpoint = "/endpoint/url"
    api_client.client = MockClient(
        url_contains=[endpoint, "http://127.0.0.1"],
        kwargs_props={"headers": {"Authorization": f"Bearer {tok}"}},
    )
    await api_client._get(endpoint, token=tok)
    await api_client._post(endpoint, token=tok)


@pytest.mark.asyncio
async def test_register():
    api_client = QuizlyAPI("http://127.0.0.1")
    tok = "Defgtg"
    id = "Ddffdf"
    api_client.client = MockClient(
        url_contains=[id, tok, "http://127.0.0.1", "/redeem_token"]
    )
    await api_client.register_token(tok, id)


@pytest.mark.asyncio
async def test_auth_token():
    api_client = QuizlyAPI("http://127.0.0.1")
    id = "Ddffdf"
    api_client.client = MockClient(
        url_contains=[id, "http://127.0.0.1", "/get_auth_token_telegram"]
    )
    await api_client.get_auth_token(id)
