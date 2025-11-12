# task-service/app/infrastructure/auth_utils.py

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.settings import settings

# Контекст паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    """Создает JWT токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """Хэширует пароль"""
    return pwd_context.hash(password)