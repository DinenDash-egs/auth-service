from fastapi import FastAPI
from auth.routes import router as auth_router
from config import settings

app = FastAPI(title="Dine & Dash Authentication Service")

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dine & Dash Authentication Service!"}