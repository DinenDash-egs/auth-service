from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

class UserModel(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
