from jose import jwt, JWTError
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from typing import Dict, Any

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str, secret_key: str, algorithms: list) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def extract_user_info(token: str, secret_key: str, algorithms: list) -> Dict[str, Any]:
    payload = verify_token(token, secret_key, algorithms)
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
        "name": payload.get("name")
    }