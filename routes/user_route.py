"""
original author: Dominik Cedro
created: 2024-06-05
license: BSD 3.0
description: fastAPI routing for users
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError
from starlette.responses import JSONResponse

from models.users import User, Stroop, DigitSubstitution, TrailMaking, UpdateUserRequest
from database.database import collection_users, collection_counters, collection_auth
from schema.schemas import user_serial_list, user_serial_single
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import ValidationError
from starlette.responses import JSONResponse

from models.users import User, Stroop, DigitSubstitution, TrailMaking
from database.database import collection_users, collection_counters
from schema.schemas import user_serial_list, user_serial_single
from security.security_config import get_current_user, TokenData, get_password_hash

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

### users collection
# GET
@user_router.get("/all_users")
async def get_users():
    users = user_serial_list(collection_users.find())
    return users

@user_router.get("/me")
async def get_my_user(current_user: TokenData = Depends(get_current_user)):
    user_id = current_user.user_id
    result = collection_users.find_one({"user_id": user_id})
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    else:
        result = user_serial_single(result)
    return result

@user_router.put("/me")
async def update_my_user(update_user_request: UpdateUserRequest, current_user: TokenData = Depends(get_current_user)):
    user_id = current_user.user_id
    user_in_db = collection_users.find_one({"user_id": user_id})
    if user_in_db is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    else:
        update_data = update_user_request.dict(exclude_unset=True)
        collection_users.update_one({"user_id": user_id}, {"$set": update_data})

        if 'email' in update_data:
            collection_auth.update_one({"user_id": user_id}, {"$set": {"email": update_data["email"]}})
        if 'password' in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
            collection_auth.update_one({"user_id": user_id}, {"$set":{"password": update_data["password"]}})


        return {"message": "User updated successfully"}



async def validation_exception_handler(request: Request, exc: ValidationError):
    errors = exc.errors()
    formatted_errors = []
    for error in errors:
        loc = error['loc']
        msg = error['msg']
        formatted_errors.append(f"Field {loc[-1]} is incorrect: {msg}")
    return JSONResponse(
        status_code=422,
        content={"message": formatted_errors}
    )

def get_next_sequence_value(sequence_name):
    """
   util function to provide auto incremented IDs for users and evaluations
    """
    result = collection_counters.find_one({"_id": sequence_name})

    if result is None:
        collection_counters.insert_one({"_id": sequence_name, "seq": 0})

    result = collection_counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        return_document=True
    )
    return result["seq"]

