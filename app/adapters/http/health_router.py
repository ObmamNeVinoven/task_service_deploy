# task-service/app/adapters/http/health_router.py

from fastapi import APIRouter
from pymongo import MongoClient
from app.settings import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    """Простая проверка, что сервис жив."""
    return {"status": "ok"}

@router.get("/health/db")
def health_check_db():
    """
    Проверка соединения с MongoDB (требование задания ).
    """
    try:
        # Создаем временный клиент (с таймаутом 5 сек)
        client = MongoClient(
            settings.MONGO_URI, 
            serverSelectionTimeoutMS=5000
        )
        # Проверяем связь
        client.admin.command('ping')
        return {"status": "ok", "db_connection": "successful"}
    except Exception as e:
        # Если не удалось, возвращаем ошибку
        return {"status": "error", "db_connection": "failed", "detail": str(e)}