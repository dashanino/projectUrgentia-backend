import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    import os
from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=100)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_TOKEN_LOCATION = ["headers"]
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:4200"
    ).split(",")

    PUBLIC_REGISTRATION = (
        os.getenv("PUBLIC_REGISTRATION", "true").lower() == "true"
    )