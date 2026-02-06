from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    SERVICE_NAME: str = "access-control-service"

    class Config:
        env_file = ".env"

settings = Settings()
