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
        "date_taken": str(evaluation["date_taken"])
    }

# deserialaize multiple
def evaluation_serial_list(evaluations)->list:
    return[evaluation_serial_single(evaluation) for evaluation in evaluations]

### users

def user_serial_single(user) -> dict:
    return{
        "user_id": int(user["user_id"]),
    "first_name": str(user["first_name"]),
    "last_name": str(user["last_name"]),
    "version": int(user["version"]),
    "email": str(user["email"]),
    "test_ids": [int(test_id) for test_id in user.get("test_ids", [])]
    }

def user_serial_list(users)->list:
    return[user_serial_single(user) for user in users]
