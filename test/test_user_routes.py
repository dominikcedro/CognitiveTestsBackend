"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: Testing routes module and CRUD operations
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database.database import setup_connection_db, collection_users, check_for_collection_counters_null,collection_counters

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
    check_for_collection_counters_null()

    try:
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
        assert response.json() == {"message": "user created"}
    finally:
        collection_users.drop()


def test_get_user_not_found():

    collection_users.drop()
    response = client.get(f"/users/{USER_ID_NOT_EXISTING}")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}


def test_delete_user_not_found():
    collection_users.drop()
    response = client.delete(f"/users/{USER_ID_NOT_EXISTING}")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found (delete)"}


def test_post_user_conflict_id():
    check_for_collection_counters_null()
    try:
        test_user = {
            "user_id": f"{CONFLICT_ID}",
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "string@email.com",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        client.post("/users", json=test_user)
        response = client.post("/users", json=test_user)
        assert response.status_code == 409
        assert response.json() == {'detail': 'User with email string@email.com already exists'}
        # TODO magic number to delete later
    finally:
        collection_counters.drop()
        collection_users.drop()


def test_post_user_conflict_email():
    check_for_collection_counters_null()
    try:
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
    finally:
        collection_users.drop()
        collection_counters.drop()



def test_post_incorrect_form_name():
    try:
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
    finally:
        collection_users.drop()

def test_post_incorrect_form_last_name():
    try:

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
    finally:
        collection_users.drop()

def test_post_incorrect_form_email_TYPE():
    try:

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
    finally:
        collection_users.drop()


def test_post_invalid_email():
    try:

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
    finally:
        collection_users.drop()
