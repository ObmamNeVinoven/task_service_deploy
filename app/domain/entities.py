from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# Это наша основная бизнес-модель (из models.py)
class Assignment(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str = "pending"
    course_id: Optional[str] = None
    user_id: Optional[str] = None