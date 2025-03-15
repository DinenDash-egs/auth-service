from fastapi import FastAPI
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Authentication service"
)

# CORS (aceitar requests do front end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth route
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Auth service is running"}
