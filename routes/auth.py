from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from models import UserCreate, UserModel, VerifyEmailRequest, LoginRequest, UserResponse
from database import users_collection
from core.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from email_service import send_verification_email
from datetime import datetime, timedelta
import jwt
import random

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=UserModel, summary="User Registration", tags=["Authentication"])
async def register_user(user: UserCreate):
    """
    Register a new user.

    - **username**: The user username.
    - **email**: The user email (unique).
    - **password**: The user password.
    - **user_type**: 0 for normal users, 1 for couriers.
    
    Returns the created user.
    """
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    verification_code = str(random.randint(100000, 999999))
    hashed_password = hash_password(user.password)

    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "verification_code": verification_code,
        "is_verified": False,
        "user_type": user.user_type,
        "created_at": datetime.utcnow()
    }
    result = await users_collection.insert_one(new_user)

    email_sent = send_verification_email(user.email, verification_code)
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed sending the verification code")

    return UserModel(id=str(result.inserted_id), **new_user)

@router.post("/verify-email", summary="Verify User Email", tags=["Authentication"])
async def verify_email(request: VerifyEmailRequest):
    """
    Verify the user email with a verification code that's send to the email.

    - **email**: The email to verify.
    - **code**: The verification code sent via email.
    
    Returns success message if the email can be verified.
    """
    user = await users_collection.find_one({"email": request.email})
    if not user or user["verification_code"] != request.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    await users_collection.update_one(
        {"email": request.email},
        {"$set": {"is_verified": True, "verification_code": None}}
    )

    return {"message": "Email successfully verified"}

@router.post("/login", summary="User Login", tags=["Authentication"])
async def login(user: LoginRequest):
    """
    Authenticate a user and return a temporary access token.

    - **email**: The user registered email.
    - **password**: The user password.
    
    Returns a JWT access token if authentication is successful.
    """
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not db_user.get("is_verified", False):
        raise HTTPException(status_code=400, detail="Email not verified")

    access_token = create_access_token(data={"sub": db_user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/user/{username}", response_model=UserResponse, summary="Get User Info", tags=["User Information"])
async def get_user_info(username: str):
    """
    Retrieve user information by username.

    - **username**: The username of the user.
    
    Returns the user's public information.
    """
    user = await users_collection.find_one({"username": username})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "is_verified": user["is_verified"],
        "user_type": user["user_type"],
        "created_at": user["created_at"]
    }
