"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: fastAPI routing for evaluations
"""
from fastapi import APIRouter
from models.evaluations import Evaluation
from models.users import User
from database.database import collection_evaluations, collection_users, collection_counters, check_for_collection_counters_null
from schema.schemas import evaluation_serial_list, user_serial_list
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.users import User, Stroop, DigitSubstitution, TrailMaking
from routes.user_route import get_next_sequence_value


evaluations_router = APIRouter()

### Evaluations - > embedded in User# POST
@evaluations_router.post("/stroop/{user_id}")
async def post_stroop(user_id: int, stroop: Stroop):
    """
    POST operation on STROOP evaluation for selected user
    """
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"stroop": dict(stroop)}}
    )
    return {"message": "Stroop test posted successfully"}

@evaluations_router.post("/trailmaking/{user_id}")
async def post_trailmaking(user_id: int, trailmaking: TrailMaking):
    """
    POST operation on TRAIL MAKING evaluation for selected user
    """
    check_for_collection_counters_null()
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")


    trail_making = dict(trailmaking)
    print(trail_making)
    trail_making["trail_making_id"] = get_next_sequence_value("trailmaking_id")
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"trail_making": trail_making}}
    )
    return {"message": "Trail Making test posted successfully"}

@evaluations_router.post("/digitsubstitution/{user_id}")
async def post_digitsubstitution(user_id: int, digitsubstitution: DigitSubstitution):
    """
    POST operation on DIGIT SUBSTITUTION evaluation for selected user
    """

    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
    digit_substitution = dict(digitsubstitution)
    digit_substitution["digit_sub_id"] = get_next_sequence_value("digit_sub_id")
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"digit_substitution": digit_substitution}}
    )
    return {"message": "Digit-Substitution posted successfully"}

# @evaluations_router.get("/digitsubstitution/{user_id}")
# async def post_digitsubstitution(user_id: int):
#     """
#     GET operation on DIGIT SUBSTITUTION evaluation for selected user to get all in list
#     """
#     user = collection_users.find_one({"user_id": user_id})
#     if user is None:
#         raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
#     return user.get("digit_substitution", [])

#
# @evaluations_router.get("/digitsubstitution/{user_id}")
# async def post_digitsubstitution(user_id: int):
#     """
#     GET operation on DIGIT SUBSTITUTION evaluation for selected user to get all in list
#     """
#     user = collection_users.find_one({"user_id": user_id})
#     if user is None:
#         raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
#     return user.get("digit_substitution", [])
#
#
# @evaluations_router.get("/digitsubstitution/{user_id}")
# async def post_digitsubstitution(user_id: int):
#     """
#     GET operation on DIGIT SUBSTITUTION evaluation for selected user to get all in list
#     """
#     user = collection_users.find_one({"user_id": user_id})
#     if user is None:
#         raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
#     return user.get("digit_substitution", [])


@evaluations_router.get("/evaluations/{user_id}")
async def get_all_evaluations(user_id: int):
    """
    GET operation on ALL evaluations for selected user to get all in list
    """
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
    stroop = user.get("stroop", [])
    digit_sub = user.get("digit_substitution", [])
    trail_make = user.get("trail_making", [])
    result = stroop + digit_sub + trail_make
    return result
