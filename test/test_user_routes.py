"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: Testing routes module and CRUD operations
"""

from fastapi.testclient import TestClient
from main import app
from database.database import setup_connection_db

client = TestClient(app)

USER_ID_NOT_EXISTING = 9999
USER_ID_ALREADY_EXISTING = 2
USER_ID_TO_CREATE = 1
REPEATED_EMAIL = "repeated_email@mail.com"
CONFLICT_ID = 3


def test_get_users_empty():
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json() == []


def test_post_user():
        test_user = {
            "user_id": USER_ID_TO_CREATE,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "string",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        response = client.post("/users", json=test_user)
        client.delete(f"/users/{USER_ID_TO_CREATE}")
        assert response.status_code == 200
        assert response.json() == {"msg": "user created"}


def test_get_user_not_found():
        response = client.get(f"/users/{USER_ID_NOT_EXISTING}")
        assert response.status_code == 404
        assert response.json() == {"msg" : "user not found (get fail)"}


def test_delete_user_not_found():
    response = client.get(f"/users/{USER_ID_NOT_EXISTING}")
    assert response.status_code == 404
    assert response.json() == {"msg": "user not found (delete fail)"}


def test_post_user_conflict_id():
    test_user = {
        "user_id": f"{CONFLICT_ID}",
        "first_name": "string",
        "last_name": "string",
        "version": 0,
        "email": "string",
        "stroop": [],
        "digit_substitution": [],
        "trail_making": []
    }
    client.post("/users", json=test_user)
    response = client.post("/users", json=test_user)
    assert response.status_code == 409
    assert response.json() == {"msg": "user with same email already exists"}


def test_post_user_conflict_email():
        test_user = {
            "user_id": 0,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": f"{REPEATED_EMAIL}", # TODO fix magic number repeated email
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        client.post("/users", json=test_user)
        response = client.post("/users", json=test_user)
        assert response.status_code == 409
        assert response.json() == {"msg" : "user with same email already exists"}


def test_post_incorrect_form():
    test_user = {
        "user_id": 0,
        "first_name": "string",
        "last_name": "string",
        "version": 0,
        "email": f"{REPEATED_EMAIL}",  # TODO fix magic number repeated email
        "stroop": [],
        "digit_substitution": [],
        "trail_making": []
    }
    response = client.post("/users", json=test_user)
    response = client.post("/users", json=test_user)
    assert response.status_code == 409
    assert response.json() == {"detail": f"User with email {REPEATED_EMAIL} already exists"}


