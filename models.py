from pydantic import BaseModel, EmailStr, Field
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
    user_type: int = Field(0, ge=0, le=1)  # 0 = Normal User, 1 = Courier
    created_at: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
        json_encoders = {ObjectId: str}

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: int = Field(0, ge=0, le=1)

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_verified: bool
    user_type: int
    created_at: datetime
