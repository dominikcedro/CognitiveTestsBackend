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

#type checks for USER forms
INCORRECT_TYPE_FIRST_NAME = 123
INCORRECT_TYPE_LAST_NAME = 123
INCORRECT_TYPE_MAIL = 123
INCORRECT_TYPE_STRING_MAIL = "email.email"
INCORRECT_TYPE_STROOP = "list"
INCORRECT_TYPE_DIGIT_SUB = "list"
INCORRECT_TYPE_TRAIL_MAKING = "list"


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
            "email": "correct_email@mail.com",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        response = client.post("/users", json=test_user)
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
        "email": f"{REPEATED_EMAIL}",
        "stroop": [],
        "digit_substitution": [],
        "trail_making": []
    }
    client.post("/users", json=test_user)
    response = client.post("/users", json=test_user)
    assert response.status_code == 409
    assert response.json() == {"detail": f"User with email {REPEATED_EMAIL} already exists"}


def test_post_incorrect_form_name():
    test_user = {
        "user_id": 0,
        "first_name": INCORRECT_TYPE_FIRST_NAME,  # Invalid type
        "last_name": "string",
        "version": 0,
        "email": "test@example.com",
        "stroop": [],
        "digit_substitution": [],
        "trail_making": []
    }
    response = client.post("/users", json=test_user)
    assert response.status_code == 422
    detail = response.json()["detail"]
    print(detail)
    assert any(error["loc"][-1] == "first_name" and "Input should be a valid string" in error["msg"] for error in detail)


def test_post_incorrect_form_last_name():
    test_user = {
        "user_id": 0,
        "first_name": "string",
        "last_name": INCORRECT_TYPE_LAST_NAME,
        "version": 0,
        "email": "test@example.com",
        "stroop": [],
        "digit_substitution": [],
        "trail_making": []
    }
    response = client.post("/users", json=test_user)
    assert response.status_code == 422
    detail = response.json()["detail"]
    print(detail)
    assert any(error["loc"][-1] == "last_name" and "Input should be a valid string" in error["msg"] for error in detail)


def test_post_incorrect_form_email_TYPE():
    test_user = {
        "user_id": 0,
        "first_name": "string",
        "last_name": "string",
        "version": 0,
        "email": INCORRECT_TYPE_MAIL,
        "stroop": [],
        "digit_substitution": [],
        "trail_making": []
    }
    response = client.post("/users", json=test_user)
    assert response.status_code == 422
    detail = response.json()["detail"]
    print(detail)
    assert any(error["loc"][-1] == "email" and "Input should be a valid string" in error["msg"] for error in detail)

def test_post_invalid_email():
    test_user = {
        "user_id": 0,
        "first_name": "string",
        "last_name": "string",
        "version": 0,
        "email": INCORRECT_TYPE_STRING_MAIL,
        "stroop": [],
        "digit_substitution": [],
        "trail_making": []
    }
    response = client.post("/users", json=test_user)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any(error["loc"][-1] == "email" and "value is not a valid email address" in error["msg"] for error in detail)