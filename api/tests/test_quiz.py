from app.schemas.quiz import (
    CreateQuizSchema,
    GetAttemptsPaginatedSchema,
    GetGameSchema,
    GetQuizesPaginatedSchema,
    GetQuizSchema,
)
from fastapi.testclient import TestClient

from .common import bearer, create_game, create_quiz, good_questions, register


def test_create_quiz(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp, data = create_quiz(
        app, resp["access_token"], resp["id"], questions=good_questions
    )
    assert resp.ok
    resp = CreateQuizSchema(**resp.json())
    resp.timestamp = 0
    assert resp == data


def test_create_quiz_no_q(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp, data = create_quiz(app, resp["access_token"], resp["id"], questions=[])
    assert resp.status_code == 400


def test_delete_quiz(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    access_token = resp["access_token"]
    resp, _ = create_quiz(app, access_token, resp["id"], questions=good_questions)
    resp = resp.json()
    resp = app.delete(
        f"/api/quiz/{resp['id']}/delete",
        headers=bearer(access_token),
    )
    assert resp.ok
    assert resp.json()["message"] == "successful"


def test_get_quiz(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    access_token = resp["access_token"]
    resp, data = create_quiz(app, access_token, resp["id"], questions=good_questions)
    resp = resp.json()
    resp = app.get(
        f"/api/quiz/quiz/{resp['id']}",
        headers=bearer(access_token),
    )
    assert resp.ok
    resp = CreateQuizSchema(**resp.json())
    resp.timestamp = 0
    assert resp == data


def test_empty_leaderboard(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    access_token = resp["access_token"]
    resp, data = create_quiz(app, access_token, resp["id"], questions=good_questions)
    resp = resp.json()
    resp = app.get(
        f"/api/quiz/{resp['id']}/leaderboard",
        headers=bearer(access_token),
    )
    assert resp.ok
    resp = GetAttemptsPaginatedSchema(**resp.json())
    assert resp == GetAttemptsPaginatedSchema(
        per_page=20, page=1, data=[], has_next=False
    )


def test_quizes(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    access_token = resp["access_token"]
    id = resp["id"]
    resp, data1 = create_quiz(app, access_token, id, questions=good_questions)
    resp, data2 = create_quiz(app, access_token, id, questions=good_questions)
    resp = resp.json()
    resp = app.get(
        "/api/quiz/quizes",
        headers=bearer(access_token),
    )
    assert resp.ok
    resp = GetQuizesPaginatedSchema(**resp.json())
    data1 = GetQuizSchema(id=resp.data[0].id, **data1.dict())
    data1.timestamp = resp.data[0].timestamp
    data2 = GetQuizSchema(id=resp.data[1].id, **data2.dict())
    data2.timestamp = resp.data[1].timestamp
    assert resp == GetQuizesPaginatedSchema(
        per_page=8, page=1, data=[data1, data2], has_next=False
    )


def test_launch(app: TestClient):
    resp, quiz_id, data, _ = create_game(app)
    assert resp.ok
    resp = resp.json()
    assert resp["quiz_id"] == quiz_id and resp["creator_id"] == data.creator_id


def test_join(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    access_token = resp["access_token"]
    creator_id = resp["id"]
    resp, data = create_quiz(app, access_token, creator_id, questions=good_questions)
    resp = resp.json()
    quiz_id = resp["id"]
    resp = app.get(
        f"/api/quiz/{quiz_id}/join",
        headers=bearer(access_token),
    )
    assert resp.ok
    resp = resp.json()
    assert resp["quiz_id"] == quiz_id and resp["creator_id"] == data.creator_id


def test_get_game(app: TestClient):
    resp, quiz_id, data, access_token = create_game(app)
    resp = app.get(
        f"/api/quiz/game/{resp.json()['game_id']}",
        headers=bearer(access_token),
    )
    assert resp.ok
    resp = GetGameSchema(**resp.json())
    assert len(resp.members) == 1
