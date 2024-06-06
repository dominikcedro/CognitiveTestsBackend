"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: Testing routes module and CRUD operations
"""

from fastapi.testclient import TestClient
from pymongo import MongoClient

from main import app  # import your FastAPI application
import unittest
from database.database import setup_connection_db

client = TestClient(app)

USER_ID_NOT_EXISTING = 9999
USER_ID_ALREADY_EXISTING = 2
USER_ID_TO_CREATE = 1

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up test database
        setup_connection_db('test_database_config.json')

    @classmethod
    def tearDownClass(cls):
        # Tear down test database
        client = MongoClient(setup_connection_db('test_database_config.json'))
        client.drop_database('TestDatabase')
    def test_get_users(self):
        response = client.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_post_user(self):
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
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), test_user)

    def test_get_user_not_found(self):
        response = client.get(f"/users/{USER_ID_NOT_EXISTING}")
        self.assertEqual(response.status_code, 404)

    def test_delete_user_not_found(self):
        response = client.delete(f"/users/{USER_ID_NOT_EXISTING}")
        self.assertEqual(response.status_code, 404)

    def test_post_user_conflict_id(self):
        test_user = {
            "user_id": USER_ID_ALREADY_EXISTING,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "string",
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        response = client.post("/users", json=test_user)
        self.assertEqual(response.status_code, 409)

    def test_post_user_conflict_email(self):
        test_user = {
            "user_id": 0,
            "first_name": "string",
            "last_name": "string",
            "version": 0,
            "email": "repeated_email", # TODO fix magic number repeated email
            "stroop": [],
            "digit_substitution": [],
            "trail_making": []
        }
        response = client.post("/users", json=test_user)
        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
