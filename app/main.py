from fastapi import FastAPI
from app.adapters.http import auth_router, items_router, health_router
from app.settings import settings

app = FastAPI(title="Task Service (Refactored)")

# Подключаем роутеры
app.include_router(health_router.router)
app.include_router(auth_router.router)
app.include_router(items_router.router)

@app.get("/")
def root():
    return {"message": "Task Service is running"}