"""
original author: Dominik Cedro
created: 2024-06-05
license: BSD 3.0
description: fastAPI routing for users
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError
from starlette.responses import JSONResponse

from models.users import User, Stroop, DigitSubstitution, TrailMaking
from database.database import collection_users, collection_counters
from schema.schemas import user_serial_list

user_router = APIRouter()

def get_next_sequence_value(sequence_name):
    result = collection_counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        return_document=True
    )
    return result["seq"]

### users collection
# GET
@user_router.get("/users")
async def get_users():
    users = user_serial_list(collection_users.find())
    return users

# POST
@user_router.post("/users")
async def post_user(user: User):
    user_dict = dict(user)
    user_dict["user_id"] = get_next_sequence_value("user_id")
    existing_user = collection_users.find_one({"user_id": user_dict["user_id"]})
    if existing_user is not None:
        raise HTTPException(status_code=409, detail=f"User with ID {user_dict['user_id']}already exists")
    existing_user_email = collection_users.find_one({"email": user_dict["email"]})
    if existing_user_email is not None:
        raise HTTPException(status_code=409, detail=f"User with email {user_dict['email']} already exists")

    collection_users.insert_one(user_dict)
    return user


async def validation_exception_handler(request: Request, exc: ValidationError):
    errors = exc.errors()
    formatted_errors = []
    for error in errors:
        loc = error['loc']
        msg = error['msg']
        formatted_errors.append(f"Field {loc[-1]} is incorrect: {msg}")
    return JSONResponse(
        status_code=422,
        content={"detail": formatted_errors}
    )


# DELETE
@user_router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    result = collection_users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}