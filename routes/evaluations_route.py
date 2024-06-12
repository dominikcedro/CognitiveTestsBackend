"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: fastAPI routing for evaluations
"""
from fastapi import APIRouter, Depends
from models.evaluations import PostStroopRequest, PostTrailMakingRequest
from models.users import User
from database.database import collection_evaluations, collection_users, collection_counters, check_for_collection_counters_null
from schema.schemas import evaluation_serial_list, user_serial_list
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.users import User, Stroop, DigitSubstitution, TrailMaking
from routes.user_route import get_next_sequence_value


evaluations_router = APIRouter()

from security.security_config import get_current_user, TokenData

@evaluations_router.post("/stroop")
async def post_stroop(stroop_request: PostStroopRequest, current_user: TokenData = Depends(get_current_user)):
    """
    POST operation on STROOP evaluation for selected user
    """
    user_id = current_user.user_id
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
    stroop_id = get_next_sequence_value("stroop_id")
    stroop_in_db = {
    "stroop_id": stroop_id,
    "version": 1, # TODO what do i need it for?
    "datetime": stroop_request.datetime,
    "mistake_count": stroop_request.mistake_count,
    "total_score": stroop_request.total_score
}
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"stroop": stroop_in_db}}
    )
    return {"message": "Stroop test posted successfully"}

@evaluations_router.post("/trailmaking")
async def post_trailmaking(trail_making_request: PostTrailMakingRequest, current_user: TokenData = Depends(get_current_user)):
    """
    POST operation on TRAIL MAKING evaluation for selected user
    """
    user_id = current_user.user_id
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} doesn't exist")
    trail_making_id = get_next_sequence_value("trailmaking_id")
    trail_making_in_db = { # TODO change to model using model from evaluations file
        "stroop_id": trail_making_id,
        "version": 1,  # TODO what do i need it for?
        "datetime": trail_making_request.datetime,
        "mistake_count": trail_making_request.mistake_count,
        "total_score": trail_making_request.total_score
    }
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"trail_making": trail_making_in_db}}
    )
    return {"message": f"Trail Making test posted successfully with id: {trail_making_in_db}"}

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
