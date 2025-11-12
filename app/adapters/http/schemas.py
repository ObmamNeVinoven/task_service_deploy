from pydantic import BaseModel
from typing import Optional
from datetime import datetime  # <-- ДОБАВЬ ЭТУ СТРОКУ
from app.domain.entities import Assignment 

# Схема для создания (из auth.py)
class UserCreateSchema(BaseModel):
    email: str
    password: str

# Схема для ответа токена (из main.py)
class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str

# Схема для создания Assignment (из main.py)
class AssignmentCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str = "pending"
    course_id: Optional[str] = None

# Схема для ответа Assignment (из domain.entities)
class AssignmentResponseSchema(Assignment):
    pass

# Схема для обновления статуса
class StatusUpdateSchema(BaseModel):
    status: str