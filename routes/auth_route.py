from fastapi import APIRouter

from models.auth import UserAuth, UserLoginRequest
from database.database import collection_auth
from security.security_config import get_password_hash, verify_password
####
auth_route = APIRouter()

# POST
@auth_route.post("/register")
async def post_user(create_user_request: UserAuth):
    user_dict = dict(create_user_request)
    print(user_dict["password"])
    password = user_dict["password"]
    user_dict["password"] = get_password_hash(password)
    print(user_dict["password"])
    collection_auth.insert_one(user_dict)
    return {"message": "user created hooray!"}

@auth_route.post("/login")
async def login_user(login_request: UserLoginRequest):
    user_dict = dict(login_request)
    login_email = user_dict["email"]
    login_password = user_dict["password"]
    # first check for existing user
    user_in_db = collection_auth.find_one({"email": login_email})
    password_in_db = user_in_db["password"]
    result = verify_password(login_password,password_in_db)
    if result:
        return {"message": "user logged in!"}
    else:
        return {"message": "not successful ;-("}

