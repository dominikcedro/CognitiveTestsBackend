"""
original author: Dominik Cedro
created: 2024-05-22
license: BSD 3.0
description: This module contains database setup for MongoDB cluster
"""
import os
import json
from pymongo import MongoClient

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
# collection for storing details about evaluations
collection_evaluations = db["evaluations"]
# collection for storing users and their respective tests
collection_users = db["users"]
# collection for counters regarding IDs for users and evaluations
collection_counters = db["counters"]
# After initializing the collection_counters
if collection_counters.count_documents({}) == 0:  # Check if the collection is empty
    collection_counters.insert_many([
        {"_id": "user_id", "seq": 0},
        {"_id": "test_id", "seq": 0}
    ])