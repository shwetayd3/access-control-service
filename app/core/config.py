from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    SERVICE_NAME: str = "access-control-service"

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/access_control"
    )

    class Config:
        env_file = ".env"

settings = Settings()
