from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    auth0_id: Optional[str] = None  # ID do usuário no Auth0
    created_at: Optional[str] = None  # Data de criação do usuário
    updated_at: Optional[str] = None  # Data da última atualização do usuário

    class Config:
        orm_mode = True