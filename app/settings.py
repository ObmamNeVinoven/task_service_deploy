from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Из database.py
    MONGO_URI: str = "mongodb://mongo:27017"
    DB_NAME: str = "taskdb"
    
    # Из auth.py
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Из main.py и crud.py
    PET_SERVICE_URL: str = "http://pet-service:8000"
    NOTIFICATION_SERVICE_URL: str = "http://notification-service:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Синглтон-экземпляр настроек
settings = Settings()