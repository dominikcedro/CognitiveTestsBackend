import unittest
from pymongo import MongoClient
from app.config.database import setup_connection_db

class TestDatabase(unittest.TestCase):
    def test_connection(self):
        uri = setup_connection_db()
        client = MongoClient(uri)
        self.assertIsNotNone(client)

if __name__ == '__main__':
    unittest.main()