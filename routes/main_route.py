"""
original author: Dominik Cedro
created: 2024-06-05
license: BSD 3.0
description: fastAPI routing for users
"""
from fastapi import APIRouter, HTTPException
from models.users import User, Stroop, DigitSubstitution, TrailMaking
from database.database import collection_users, collection_counters
from schema.schemas import user_serial_list

main_router = APIRouter()

@main_router.get("/")
async def get_healthcheck():
    return {"healthcheck": "test-if-it-works"}

