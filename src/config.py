import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-auth0-domain")
    API_IDENTIFIER = os.getenv("API_IDENTIFIER", "your-api-identifier")
    API_AUDIENCE = os.getenv("API_AUDIENCE", "your-api-audience")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHMS = ["RS256"]