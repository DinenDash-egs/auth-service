from fastapi import FastAPI
from routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Authentication service",
    version="1.0",
    root_path="/auth"
)

# CORS (aceitar requests do front end)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://grupo8-egs.deti.ua.pt"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth route
app.include_router(auth_router, prefix="/v1")

@app.get("/")
def root():
    return {"message": "Auth service is running"}
