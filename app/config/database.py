from pymongo import MongoClient
import os
import json



def setup_connection_db():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(dir_path, 'database_config.json')
    with open(config_path) as f:
        config = json.load(f)
    username = config['username']
    password = config['password']

    uri = f"mongodb+srv://{username}:{password}@cognitivetests.fsbiorm.mongodb.net/?retryWrites=true&w=majority&appName=CognitiveTests"
    return uri


uri = setup_connection_db()
client = MongoClient(uri)

db = client.todo_db

collection_name = db["todo_collection"]