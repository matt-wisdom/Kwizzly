from core.helpers.cache import RedisBackend
from fastapi.testclient import TestClient

from .common import create_game, good_questions, register
from .play import play_game, play_game_slow

redis = RedisBackend()


def main(
    app: TestClient,
    token: str,
    quiz_id: str,
    questions: list,
    q_answer="ok",
    slow=False,
):
    """
    Listen for new game request and create websocket session
    for each request.
    """
    with app.websocket_connect(
        f"/game/singleplayer?token={token}&quiz_id={quiz_id}"
    ) as ws:
        if slow:
            return play_game_slow(ws, questions, q_answer)
        else:
            return play_game(ws, questions, q_answer)


def test_single(app):
    resp, quiz_id, data, token = create_game(app)
    assert resp.ok
    resp = resp.json()
    finished = main(app, token, resp["quiz_id"], good_questions)
    assert finished["data"]["correct"] == 10
    assert finished["data"]["score"] == 100


def test_single_all_wrong(app):
    resp, quiz_id, data, token = create_game(app)
    assert resp.ok
    resp = resp.json()
    finished = main(app, token, resp["quiz_id"], good_questions, q_answer="ff")
    assert finished["data"]["correct"] == 0
    assert finished["data"]["score"] == 0


def test_single_some_wrong(app):
    resp, quiz_id, data, token = create_game(app)
    assert resp.ok
    resp = resp.json()
    finished = main(app, token, resp["quiz_id"], good_questions, q_answer=["ff", "ok"])
    assert finished["data"]["correct"] == 5
    assert finished["data"]["score"] == 50


def test_single_timeout(app):
    resp, quiz_id, data, token = create_game(app)
    assert resp.ok
    resp = resp.json()
    finished = main(
        app, token, resp["quiz_id"], good_questions, q_answer=["ff", "ok"], slow=True
    )
    assert finished["data"]["correct"] == 4
    assert finished["data"]["score"] == 40
