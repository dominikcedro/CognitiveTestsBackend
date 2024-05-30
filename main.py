"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: This module contains main fastAPI app that runs backend for CognitiveTests mobile app.
"""

from fastapi import FastAPI
from routes.route import router

app = FastAPI()
app.include_router(router)

