import threading
import time

from fastapi.testclient import TestClient

from .common import bearer, create_game_tok, create_quiz, good_questions, register
from .play_multi import play_as


def create_users(app: TestClient, no=2):
    user_tokens = []
    data = []
    for i in range(no):
        resp = register(app, f"test{i}@test.com").json()
        user_tokens.append(resp["access_token"])
        data.append(resp)
    return user_tokens, data


def launch(app: TestClient, access_tokens: list):

    resp, quiz_id, data, token = create_game_tok(app)
    assert resp.ok
    # resp = resp.json()
    # creator_id = resp["creator_id"]
    # resp, data = create_quiz(app, access_tokens[0], creator_id, questions=good_questions)
    # resp = resp.json()
    # quiz_id = resp["id"]
    # resp = app.get(
    #     f"/api/quiz/{quiz_id}/launch-multiplayer",
    #     headers=bearer(access_tokens[0]),
    # )
    return resp, [token, *access_tokens]


def test_multi(app: TestClient):
    toks, data = create_users(app)
    # resp, toks = launch(app, toks)
    c_id = data[0]["id"]
    resp, data = create_quiz(app, toks[0], data[0]["id"], questions=good_questions)
    resp = resp.json()
    quiz_id = resp["id"]
    resp = app.get(
        f"/api/quiz/{quiz_id}/launch-multiplayer",
        headers=bearer(toks[0]),
    )
    resp = resp.json()
    print("\n\n\nID", c_id)
    t1 = threading.Thread(
        target=play_as,
        args=(app, resp["game_id"], toks[0], resp["quiz_id"], good_questions),
        kwargs={"creator": True, "can_answer": True},
    )
    t2 = threading.Thread(
        target=play_as,
        args=(app, resp["game_id"], toks[1], resp["quiz_id"], good_questions),
        kwargs={"creator": False, "can_answer": False},
    )
    t1.start()
    time.sleep(2)
    t2.start()
    t1.join()
    t2.join()
