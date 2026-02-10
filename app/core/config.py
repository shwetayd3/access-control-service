from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    SERVICE_NAME: str = "access-control-service"

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/access_control"
    )

    JWT_SECRET_KEY: str = "change-this-in-prod"

    GOOGLE_CLIENT_ID: str

    class Config:
        env_file = ".env"

settings = Settings()
