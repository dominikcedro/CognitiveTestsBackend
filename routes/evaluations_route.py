"""
original author: Dominik Cedro
created: 2024-05-17
license: BSD 3.0
description: fastAPI routing for evaluations
"""
from fastapi import APIRouter, Depends
from models.evaluations import PostStroopRequest, PostTrailMakingRequest, PostDigitSubstitutionRequest, \
    GetAllEvaluationsResponse
from models.users import User
from database.database import collection_evaluations, collection_users, collection_counters, check_for_collection_counters_null
from schema.schemas import evaluation_serial_list, user_serial_list
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from models.users import User, Stroop, DigitSubstitution, TrailMaking
from routes.user_route import get_next_sequence_value


evaluations_router = APIRouter(
    prefix="/evaluation",
    tags=["evaluation"]
)

from security.security_config import get_current_user, TokenData

@evaluations_router.post("/stroop")
async def post_stroop(stroop_request: PostStroopRequest, current_user: TokenData = Depends(get_current_user)):
    """
    POST operation on STROOP evaluation for selected user
    """
    user_id = current_user.user_id
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "detail": f"User with ID {user_id} doesn't exist",
                "instance": "/evaluation/stroop"
            }
        )
    stroop_id = get_next_sequence_value("stroop_id")
    stroop_in_db = {
    "stroop_id": stroop_id,
    "version": 1, # TODO what do i need it for?
    "datetime": stroop_request.datetime,
    "mistake_count": stroop_request.mistake_count,
        "total_score": 1
}
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"stroop": stroop_in_db}}
    )
    return {"message": "Stroop test posted successfully"}

@evaluations_router.post("/trail_making")
async def post_trail_making(trail_making_request: PostTrailMakingRequest, current_user: TokenData = Depends(get_current_user)):
    """
    POST operation on TRAIL MAKING evaluation for selected user
    """
    user_id = current_user.user_id
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "detail": f"User with ID {user_id} doesn't exist",
                "instance": "/evaluation/stroop"
            }
        )
    trail_making_id = get_next_sequence_value("trail_making_id")
    trail_making_in_db = TrailMaking(trail_making_id=trail_making_id,version=1, datetime=trail_making_request.datetime,
                                     time=trail_making_request.time, mistake_count=trail_making_request.mistake_count,
                                     total_score=1)

    # trail_making_in_db = { # TODO change to model using model from evaluations file
    #     "trail_making_id": trail_making_id,
    #     "version": 1,1
    #     "datetime": trail_making_request.datetime,
    #     "time": trail_making_request.time,
    #     "mistake_count": trail_making_request.mistake_count
    # }
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"trail_making": dict(trail_making_in_db)}}
    )
    return {"message": f"Trail Making test posted successfully with id: {trail_making_in_db.trail_making_id}"}

@evaluations_router.post("/digit_substitution")
async def post_digit_substitution(digit_substitution_request: PostDigitSubstitutionRequest, current_user: TokenData = Depends(get_current_user)):
    """
    POST operation on DIGIT SUBSTITUTION evaluation for selected user
    """
    user_id = current_user.user_id
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "detail": f"User with ID {user_id} doesn't exist",
                "instance": "/evaluation/stroop"
            }
        )
    digit_sub_id = get_next_sequence_value("digit_substitution_id")
    digit_substitution_in_db = {
        "digit_sub_id": digit_sub_id,
        "version": 1,
        "datetime": digit_substitution_request.datetime,
        "mistake_count": digit_substitution_request.mistake_count,
        "correct_answers": digit_substitution_request.correct_answers,
        "total_score": 1
    }
    collection_users.update_one(
        {"user_id": user_id},
        {"$push": {"digit_substitution": digit_substitution_in_db}}
    )
    return {"message": f"Digit substitition test posted successfully with id: {digit_sub_id}"}

@evaluations_router.get("/all", response_model=GetAllEvaluationsResponse)
async def get_all_evaluations(current_user: TokenData = Depends(get_current_user)):
    """
    GET operation on ALL evaluations for selected user to get all in list
    """
    user_id = current_user.user_id
    user = collection_users.find_one({"user_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "detail": f"User with ID {user_id} doesn't exist",
                "instance": "/evaluation/all"
            }
        )
    stroop = user.get("stroop", [])
    digit_sub = user.get("digit_substitution", [])
    trail_make = user.get("trail_making", [])

    return GetAllEvaluationsResponse(stroop=stroop, digit_substitution=digit_sub, trail_making=trail_make)

