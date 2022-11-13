import os

import pytest
from fastapi.testclient import TestClient

os.environ["TESTING"] = "1"

from core.db import (
    attempts_db_client,
    games_db_client,
    invites_db_client,
    quiz_db_client,
    texts_db_client,
    user_db_client,
)

clients = [
    quiz_db_client,
    texts_db_client,
    attempts_db_client,
    invites_db_client,
    games_db_client,
    user_db_client,
]

from app import app as app_

for client in clients:
    client.delete({}, True)


@pytest.fixture
def app():
    yield TestClient(app_)
    for client in clients:
        client.delete({}, True)
