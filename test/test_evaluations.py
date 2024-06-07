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


def test_post_stroop():
    try:
        test_user = {
            "user_id": 1,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "correct_email@mail.com",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        client.post("/users", json=test_user)

        stroop_test = {
            "stroop_id": 1,
            "version": 1,
            "datetime": "2024-06-07T12:34:56",
            "mistake_count": 0,
            "total_score": 100
        }
        response = client.post("/stroop/1", json=stroop_test)

        assert response.status_code == 200
        assert response.json() == {"message": "Stroop test posted successfully"}
    finally:
        collection_counters.drop()
        collection_users.drop()

def test_post_trail_making():
    try:
        test_user = {
            "user_id": 1,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "correct_email@mail.com",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        client.post("/users", json=test_user)

        trail_making_test = {
            "trail_making_id": 1,
            "version": 1,
            "datetime": "2024-06-07T12:34:56",
            "time": 60,
            "mistake_count": 0,
            "total_score": 100
        }
        response = client.post("/trailmaking/1", json=trail_making_test)

        assert response.status_code == 200
        assert response.json() == {"message": "Trail Making test posted successfully"}
    finally:
        collection_counters.drop()
        collection_users.drop()

def test_post_digit_substituton():
    try:
        test_user = {
            "user_id": 1,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "correct_email@mail.com",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        client.post("/users", json=test_user)

        digit_sub_test = {
            "digit_sub_id": 1,
            "version": 1,
            "datetime": "2024-06-07T12:34:56",
            "time": 60,
            "mistake_count": 0,
            "total_score": 100
        }
        response = client.post("/digitsubstitution/1", json=digit_sub_test)

        assert response.status_code == 200
        assert response.json() == {"message": "Digit-Substitution posted successfully"}
    finally:
        collection_counters.drop()
        collection_users.drop()


def test_post_and_get_all_evaluations():
    try:
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
            "trail_making_id": 1,
            "version": 1,
            "datetime": "2024-06-07T12:34:56",
            "time": 60,
            "mistake_count": 0,
            "total_score": 100
        }

        test_user = {
            "user_id": 1,
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

        client.post("/digitsubstitution/1", json=digit_sub_test)

        client.post("/trailmaking/1", json=trail_making_test)

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
        collection_counters.drop()
        collection_users.drop()
