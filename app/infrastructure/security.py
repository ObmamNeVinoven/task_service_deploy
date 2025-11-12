# task-service/app/infrastructure/security.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from bson import ObjectId
from app.settings import settings
from app.domain.repositories import IUserRepository

# Это импорт, который раньше вызывал ошибку, но теперь он безопасен
from app.di import get_user_repo 

# Схема OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    user_repo: IUserRepository = Depends(get_user_repo)
) -> str:
    """
    Декодирует токен и возвращает ID пользователя.
    """
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
        
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise credentials_exception
        
        return str(user["_id"])
    except JWTError:
        raise credentials_exception
    except Exception:
        raise credentials_exception