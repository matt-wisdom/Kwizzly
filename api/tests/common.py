from app.schemas.quiz import CreateQuizSchema
from fastapi.testclient import TestClient


def register(
    app: TestClient,
    email="test@test.com",
    password1="test123",
    password2="test123",
    nickname="test123",
):
    resp = app.post(
        "/api/users/register",
        json={
            "email": email,
            "password1": password1,
            "password2": password2,
            "nickname": nickname,
        },
    )
    return resp


bearer = lambda token: {"Authorization": f"Bearer {token}"}

good_questions = [
    {"question": "Test", "answers": ["ok", "bn", "n ngn"], "correct": "ok"},
    {
        "question": "Hello",
        "answers": ["hi", "bull", "ok"],
        "correct": "ok",
    },
    {
        "question": "Hello again",
        "answers": ["hi", "bull", "ok"],
        "correct": "ok",
    },
    {
        "question": "New",
        "answers": ["hi", "bull", "ok"],
        "correct": "ok",
    },
    {
        "question": "Wat",
        "answers": ["hi", "bull", "ok"],
        "correct": "ok",
    },
    {
        "question": "Yep",
        "answers": ["hi", "bull", "ok"],
        "correct": "ok",
    },
    {"question": "Test ", "answers": ["ok", "no", "rand"], "correct": "ok"},
    {"question": "Test", "answers": ["ok", "ya", "rand"], "correct": "ok"},
    {"question": "Test ", "answers": ["ok", "no", "rand"], "correct": "ok"},
    {"question": "Test", "answers": ["ok", "ya", "rand"], "correct": "ok"},
]


def create_quiz(
    app: TestClient, access_token: str, creator_id="", title="Test", questions=[]
):
    dict_data = {
        "creator_id": creator_id,
        "public": True,
        "title": title,
        "max_contestant": 4,
        "question_per_session": 10,
        "questions": questions,
    }
    data = CreateQuizSchema(**dict_data)
    return (
        app.post("/api/quiz/create", json=data.dict(), headers=bearer(access_token)),
        data,
    )


def create_game(app):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    access_token = resp["access_token"]
    creator_id = resp["id"]
    resp, data = create_quiz(app, access_token, creator_id, questions=good_questions)
    resp = resp.json()
    quiz_id = resp["id"]
    resp = app.get(
        f"/api/quiz/{quiz_id}/launch-multiplayer",
        headers=bearer(access_token),
    )
    return resp, quiz_id, data, access_token


def create_game_tok(app):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    access_token = resp["access_token"]
    creator_id = resp["id"]
    resp, data = create_quiz(app, access_token, creator_id, questions=good_questions)
    resp = resp.json()
    quiz_id = resp["id"]
    resp = app.get(
        f"/api/quiz/{quiz_id}/launch-multiplayer",
        headers=bearer(access_token),
    )
    return resp, quiz_id, data, access_token
