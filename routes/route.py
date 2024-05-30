from fastapi import APIRouter
from models.evaluations import Evaluation
from models.users import User
from database.database import collection_evaluations, collection_users
from schema.schemas import evaluation_serial_list, user_serial_list
from bson import ObjectId
from fastapi import APIRouter, HTTPException

router = APIRouter()

### Evaluations collection

# GET
@router.get("/evaluations")
async def get_evaluations():
    evaluations = evaluation_serial_list(collection_evaluations.find())
    return evaluations

# POST
@router.post("/evaluations")
async def post_evaluation(evaluation: Evaluation):
    collection_evaluations.insert_one(dict(evaluation))
    user_id = evaluation.user_id
    if isinstance(user_id, str):
        user_id = ObjectId(user_id)

    result = collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"test_ids": evaluation.test_id}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return evaluation

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
    collection_users.insert_one(user_dict)
    return user

# DELTE
@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    result = collection_users.delete_one({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}