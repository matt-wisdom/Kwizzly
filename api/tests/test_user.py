from app.schemas.user import (
    CreateUserResponseSchema,
    GetUserResponseSchema,
    LoginResponseSchema,
)
from fastapi.testclient import TestClient

from .common import bearer, register


def test_register(app):
    resp = register(app)
    assert resp.ok
    data = CreateUserResponseSchema(**resp.json())
    assert data.email == "test@test.com" and data.nickname == "test123"


def test_register_bad_email(app):
    resp = register(app, email="test")
    assert resp.status_code == 422


def test_register_wrong(app):
    resp = register(app, "", "")
    assert resp.status_code == 422


def test_invalid_token(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp = app.get(f"/api/users/user/{resp['id']}", headers=bearer("Whatttttt"))
    assert resp.status_code == 401


def test_login(app: TestClient):
    resp = register(app, "test@test.com", "test123", "test123", "test")
    resp = app.post(
        "/api/users/login", json={"email": "test@test.com", "password": "test123"}
    )
    data = resp.json()
    assert data["email"] == "test@test.com" and data["nickname"] == "test"


def test_login_invalid_pword(app: TestClient):
    resp = register(app, "test1@test.com", "test", "test", "test1")
    resp = app.post(
        "/api/users/login", json={"email": "test1@test.com", "password": "tfddb"}
    )
    assert resp.status_code == 401
    assert resp.json()["message"] in "password invalid"


def test_login_invalid_user(app: TestClient):
    resp = register(app, "test1@test.com", "test", "test", "test1")
    resp = app.post(
        "/api/users/login", json={"email": "test@test.com", "password": "tfddb"}
    )
    assert resp.status_code == 404


def test_login_invalid_email(app: TestClient):
    resp = app.post(
        "/api/users/login", json={"email": "nonexistent@test.com", "password": "tfddb"}
    )
    assert resp.status_code == 404


def test_change_pword(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp = app.post(
        "/api/users/change-password",
        json={
            "email": "test@test.com",
            "old_password": "test",
            "new_password": "test_new",
            "new_password2": "test_new",
        },
        headers=bearer(resp["access_token"]),
    )
    assert resp.ok


def test_change_pword_wrong_old(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp = app.post(
        "/api/users/change-password",
        json={
            "email": "test@test.com",
            "old_password": "test4333",
            "new_password": "test_new",
            "new_password2": "test_new",
        },
        headers=bearer(resp["access_token"]),
    )
    assert resp.status_code == 401


def test_change_pword_wrong_nomatch(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp = app.post(
        "/api/users/change-password",
        json={
            "email": "test@test.com",
            "old_password": "test",
            "new_password": "test_ne",
            "new_password2": "test_new",
        },
        headers=bearer(resp["access_token"]),
    )
    assert resp.status_code == 401


def test_get_user(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp = app.get(
        f"/api/users/user/{resp['id']}", headers=bearer(resp["access_token"])
    )
    assert GetUserResponseSchema(**resp.json()).email == "test@test.com"


def test_myprofile(app: TestClient):
    resp = register(app, "test@test.com", "test", "test", "test").json()
    resp = app.get("/api/users/myprofile", headers=bearer(resp["access_token"]))
    assert GetUserResponseSchema(**resp.json()).email == "test@test.com"


def test_tgtoken(app: TestClient):
    resp = register(app, "test1@test.com", "test", "test", "test1").json()
    tok = resp["access_token"]
    resp = app.get("/api/users/get_telegram_token", headers=bearer(tok)).json()
    token = resp.get("token")
    assert token
    telegramid = 34554454
    resp = app.get(f"/api/users/redeem_token/{token}/{telegramid}", headers=bearer(tok))
    assert resp.ok
