from datetime import timedelta, datetime, timezone

import jwt
from fastapi import APIRouter, HTTPException, Depends

from models.auth import UserLoginRequest, UserRegisterRequest
from models.users import User
from database.database import collection_auth, collection_users
from routes.user_route import get_next_sequence_value
from security.security_config import get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, REFRESH_TOKEN_EXPIRE_DAYS, create_refresh_token, oauth2_scheme, SECRET_KEY, ALGORITHM
####
# logging
from icecream import ic
####
auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# POST
@auth_route.post("/register")
async def register_user(user_register_request: UserRegisterRequest):
    register_request = dict(user_register_request)
    register_request["password"] = get_password_hash(register_request["password"])
    user_id = get_next_sequence_value("user_id")
    ic(user_id) #### log
    user_data = {
        "user_id": user_id,
        "first_name": register_request["first_name"],
        "last_name": register_request["last_name"],
        "version": 1,
        "email": register_request["email"]
    }
    # check for existing user wieth same ID
    existing_user = collection_users.find_one({"user_id": user_data["user_id"]})
    if existing_user is not None:
        raise HTTPException(status_code=409, detail=f"User with ID {user_data['user_id']}already exists")
    # check for existing user with same email
    existing_user_email = collection_users.find_one({"email": user_data["email"]})
    if existing_user_email is not None:
        raise HTTPException(status_code=409, detail=f"User with email {user_data['email']} already exists")
    collection_users.insert_one(user_data)
    ic("user collection posted")  #### log
    user_auth = {
        "user_id": user_id,
        "email": register_request["email"],
        "password": register_request["password"]
    }
    collection_auth.insert_one(user_auth)
    ic("auth collection posted")  #### log
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user_data["email"], "user_id": user_data["user_id"]}, expires_delta=access_token_expires
    )

    # Create refresh token
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token, refresh_token_expires_date = create_refresh_token(
        data={"email": user_data["email"], "user_id": user_data["user_id"]}, expires_delta=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "refresh_token_expi": refresh_token_expires_date}

@auth_route.post("/login")
async def login_user(login_request: UserLoginRequest):
    ic("login user function operating")
    user_dict = dict(login_request)
    login_email = user_dict["email"]
    login_password = user_dict["password"]
    # first check for existing user
    user_in_db = collection_auth.find_one({"email": login_email})
    if user_in_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    password_in_db = user_in_db["password"]
    if verify_password(login_password, password_in_db):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"email": login_email, "user_id": user_in_db["user_id"]}, expires_delta=access_token_expires
        )
        access_expire = datetime.now(timezone.utc) + access_token_expires
        # Create refresh token
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token, refresh_token_expires_datetime = create_refresh_token(
            data={"email": login_email, "user_id": user_in_db["user_id"]}, expires_delta=refresh_token_expires
        )

        return {"access_token": access_token, "refresh_token": refresh_token, "refresh_token_exs": refresh_token_expires_datetime}
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

@auth_route.post("/refresh")
async def refresh_token(refresh_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        user_id: str = payload.get("user_id")
        if email is None or user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": email, "user_id": user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}