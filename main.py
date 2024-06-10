"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: This module contains main fastAPI app that runs backend for CognitiveTests mobile app.
"""

from fastapi import FastAPI
from routes.evaluations_route import evaluations_router
from routes.user_route import user_router, ValidationError, validation_exception_handler
from routes.main_route import main_router
from security.security import auth_router

app = FastAPI()
app.include_router(main_router)
app.include_router(evaluations_router)
app.include_router(user_router)
app.include_router(auth_router)
app.add_exception_handler(ValidationError, validation_exception_handler)

