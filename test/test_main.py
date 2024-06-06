"""
original author: Dominik Cedro
created: 2024-06-06
license: BSD 3.0
description: This module contains tests for main routes
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    """
    check healthcheck on main '/' route
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"healthcheck": "positive"}