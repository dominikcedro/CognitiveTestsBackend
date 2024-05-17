"""
original author: Dominik Cedro
created: 2024-05-17
license: none #TODO create license
description: This module will be testing page for mongo db connection with fast api
"""
from fastapi import FastAPI

app = FastAPI()

from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://dominocedro275:jalapeno@cognitivetests.fsbiorm.mongodb.net/?retryWrites=true&w=majority&appName=CognitiveTests"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
