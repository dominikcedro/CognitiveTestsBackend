"""
original author: Dominik Cedro
created: 2024-05-22
license: BSD 3.0
description: This module contains database setup for MongoDB cluster
"""
import os
import json
from pymongo import MongoClient
def check_for_collection_counters_null():
    if collection_counters.count_documents({}) == 0:
        collection_counters.insert_many([
            {"_id": "user_id", "seq": 0},
            {"_id": "test_id", "seq": 0}
        ])

def setup_connection_db():
    """
    This function gets configuration data from database_config.json file and connects with MongoDB
    :return:
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'database_config.json')
    with open(config_path) as f:
        config = json.load(f)
    username = config['username']
    password = config['password']

    uri = f"mongodb+srv://{username}:{password}@cognitivetests.fsbiorm.mongodb.net/?retryWrites=true&w=majority&appName=CognitiveTests"
    return uri


client = MongoClient(setup_connection_db())
db = client.CognitiveTests
collection_evaluations = db["evaluations"]
collection_users = db["users"]
collection_counters = db["counters"]
check_for_collection_counters_null()


