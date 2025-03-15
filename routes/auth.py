from fastapi import APIRouter, HTTPException, Depends
from models import UserCreate, UserModel
from database import users_collection
from core.security import hash_password
from datetime import datetime
from pymongo.errors import DuplicateKeyError

router = APIRouter()

@router.post("/register", response_model=UserModel)
async def register_user(user: UserCreate):
    # verificar se o user já existe
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="This email is already in use")

    # dar hash com bcrypt
    hashed_password = hash_password(user.password)

    # formatar para por na db
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    result = await users_collection.insert_one(new_user)
    
    # retornar o user sem a password
    return UserModel(id=str(result.inserted_id), **new_user)
