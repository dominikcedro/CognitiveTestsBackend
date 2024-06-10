"""
original author: Dominik Cedro
created: 2024-05-29
license: BSD 3.0
description: Deserialization for data stored in mongo collections to easy handle it in app
"""
from typing import List, Optional

### evaluations
# to deserialize singular evaluation
def evaluation_serial_single(evaluation) -> dict:
    return{
        "id": str(evaluation["_id"]),
        "test_id": int(evaluation["test_id"]),
        "user_id": int(evaluation["user_id"]),
        "type": str(evaluation["type"]),
        "version": int(evaluation["version"]),
        "score": int(evaluation["score"]),
        "date_taken": str(evaluation["date_taken"]),
        "custom_field_1": evaluation.get("custom_field_1"),
        "custom_field_2": evaluation.get("custom_field_2")
    }

# deserialaize multiple
def evaluation_serial_list(evaluations)->list:
    return[evaluation_serial_single(evaluation) for evaluation in evaluations]

### users
def user_serial_single(user) -> dict:
    user_dict = {
        "user_id": int(user["user_id"]),
        "first_name": str(user["first_name"]),
        "last_name": str(user["last_name"]),
        "version": int(user["version"]),
        "email": str(user["email"]),
    }

    if "stroop" in user and user["stroop"]:
        user_dict["stroop"] = user["stroop"]
    if "digit_substitution" in user and user["digit_substitution"]:
        user_dict["digit_substitution"] = user["digit_substitution"]
    if "trail_making" in user and user["trail_making"]:
        user_dict["trail_making"] = user["trail_making"]

    return user_dict

def user_serial_list(users)->list:
    return[user_serial_single(user) for user in users]
