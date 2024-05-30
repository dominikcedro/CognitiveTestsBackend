"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: fastAPI routing for users, evaluations and counter collections
"""
from fastapi import APIRouter
from models.evaluations import Evaluation
from models.users import User
from database.database import collection_evaluations, collection_users, collection_counters
from schema.schemas import evaluation_serial_list, user_serial_list
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter()
### counter collection
def get_next_sequence_value(sequence_name):
    result = collection_counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        return_document=True
    )
    return result["seq"]
### Evaluations collection

# GET
@router.get("/evaluations")
async def get_evaluations():
    evaluations = evaluation_serial_list(collection_evaluations.find())
    return evaluations

# POST
@router.post("/evaluations")
async def post_evaluation(evaluation: Evaluation):
    evaluation_dict = dict(evaluation)
    user_id = evaluation_dict["user_id"]
    existing_user = collection_users.find_one({"user_id": user_id})
    if existing_user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
    evaluation_dict["test_id"] = get_next_sequence_value("test_id")
    collection_evaluations.insert_one(evaluation_dict)
    result = collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"test_ids": evaluation_dict["test_id"]}}
    )
    return evaluation

# DELETE
@router.delete("/evaluations/{test_id}")
async def delete_evaluation(test_id: int):
    result = collection_evaluations.delete_one({"test_id": test_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return {"message": "Evaluation deleted successfully"}

### users collection
# GET
@router.get("/users")
async def get_users():
    users = user_serial_list(collection_users.find())
    return users

# POST
@router.post("/users")
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

# DELETE
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    result = collection_users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}