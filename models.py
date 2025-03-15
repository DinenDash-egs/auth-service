from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

class UserModel(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    hashed_password: str
    verification_code: str
    is_verified: bool = False
    created_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str
