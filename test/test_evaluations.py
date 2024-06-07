"""
original author: Dominik Cedro
created: 2024-06-07
license: BSD 3.0
description: testing routing for evaluations
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from database.database import setup_connection_db, collection_evaluations, collection_users, collection_counters

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

def test_post_and_get_all_evaluations():
    try:
        collection_users.drop()
        collection_counters.drop()
        if collection_counters.count_documents({}) == 0:  # Check if the collection is empty
            collection_counters.insert_many([
                {"_id": "user_id", "seq": 0},
                {"_id": "test_id", "seq": 0}
            ])
        # Create test evaluations
        stroop_test = {
            "stroop_id": 1,
            "version": 1,
            "datetime": "2024-06-07T12:34:56",
            "mistake_count": 0,
            "total_score": 100
        }

        digit_sub_test = {
            "digit_sub_id": 1,
            "version": 1,
            "datetime": "2024-06-07T12:34:56",
            "time": 60,
            "mistake_count": 0,
            "total_score": 100
        }

        trail_making_test = {
            "stroop_id": 1,
            "version": 1,
            "datetime": "2024-06-07T12:34:56",
            "time": 60,
            "mistake_count": 0,
            "total_score": 100
        }
        # create test user
        test_user = {
            "user_id": 0,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "correct_email@mail.com",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        client.post("/users", json=test_user)
        # Post the evaluations
        client.post("/stroop/1", json=stroop_test)
        client.post("/digit_substitution/1", json=digit_sub_test)
        client.post("/trail_making/1", json=trail_making_test)

        # Get all evaluations
        response = client.get("/evaluations/1")
        assert response.status_code == 200

        # Check if the evaluations are returned correctly
        evaluations = response.json()
        assert len(evaluations) == 3
        assert evaluations[0] == stroop_test
        assert evaluations[1] == digit_sub_test
        assert evaluations[2] == trail_making_test
    finally:
        # Drop the users collection after the test
        print("blab")



def test_post_user():
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
        assert response.json() == {"detail": "user created"}
    finally:
        collection_users.drop()


def test_get_user_not_found():
    collection_users.drop()
    response = client.get(f"/users/{USER_ID_NOT_EXISTING}")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not found"}