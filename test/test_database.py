"""
original author: Dominik Cedro
created: 2024-05-28
license: #TODO create license
description: This module contains tests for app/config/database.py file
"""

import unittest
from pymongo import MongoClient
from database.database import setup_connection_db
import timeout_decorator

TIMEOUT_FOR_CONNECTION_TEST = 15
class TestDatabase(unittest.TestCase):
    # @timeout_decorator.timeout(TIMEOUT_FOR_CONNECTION_TEST)
    def test_connection(self):
        uri = setup_connection_db()
        client = MongoClient(uri)
        self.assertIsNotNone(client)

if __name__ == '__main__':
    unittest.main()