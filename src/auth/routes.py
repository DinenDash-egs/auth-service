from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.utils import verify_token, create_access_token
from models.user import User
from config import AUTH0_DOMAIN, API_IDENTIFIER
import requests

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Implementar a lógica de autenticação com Auth0
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/json"}
    payload = {
        "grant_type": "password",
        "username": form_data.username,
        "password": form_data.password,
        "audience": API_IDENTIFIER,
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Invalid credentials")
    
    return response.json()

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_info

@router.post("/register")
async def register(user: User):
    # Implementar a lógica de registro de usuário
    pass

@router.get("/verify")
async def verify(token: str = Depends(oauth2_scheme)):
    user_info = verify_token(token)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"status": "verified", "user": user_info}