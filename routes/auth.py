from fastapi import APIRouter, HTTPException
from models import UserCreate, UserModel, VerifyEmailRequest
from database import users_collection
from core.security import hash_password
from email_service import send_verification_email
from datetime import datetime
import random

router = APIRouter()

@router.post("/register", response_model=UserModel)
async def register_user(user: UserCreate):
    # verificar se o email já esta na db
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    # gerar código de verificação de email
    verification_code = str(random.randint(100000, 999999))

    # dar hash à password com bcrypt
    hashed_password = hash_password(user.password)

    # estrutura para a db
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "verification_code": verification_code,
        "is_verified": False,
        "created_at": datetime.utcnow()
    }
    result = await users_collection.insert_one(new_user)

    # mandar o verification code para o email
    email_sent = send_verification_email(user.email, verification_code)
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed sending the verification code")

    return UserModel(id=str(result.inserted_id), **new_user)

@router.post("/verify-email")
async def verify_email(request: VerifyEmailRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["is_verified"]:
        raise HTTPException(status_code=400, detail="Email already verified")

    if user["verification_code"] != request.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    # dar update ao user para dizer que está verificado (poe o verification code a null e a bool a true)
    await users_collection.update_one(
        {"email": request.email},
        {"$set": {"is_verified": True, "verification_code": None}}
    )

    return {"message": "Success verifying the email"}
