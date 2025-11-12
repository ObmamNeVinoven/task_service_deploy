from app.domain.repositories import IUserRepository, IAssignmentRepository
from app.infrastructure.db import db
from bson import ObjectId
from typing import List, Dict, Any, Optional

def _assignment_serializer(assignment) -> dict:
    """Приватный сериализатор (из crud.py)"""
    if not assignment:
        return None
    return {
        "id": str(assignment["_id"]),
        "title": assignment["title"],
        "description": assignment.get("description"),
        "deadline": assignment.get("deadline"),
        "status": assignment.get("status", "pending"),
        "course_id": assignment.get("course_id"),
        "user_id": assignment.get("user_id"),
    }

class MongoUserRepository(IUserRepository):
    """Реализация репозитория пользователей (из crud.py)"""
    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return db.users.find_one({"email": email})

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            return db.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    async def create(self, email: str, hashed_password: str) -> str:
        result = db.users.insert_one({"email": email, "password": hashed_password})
        return str(result.inserted_id)

class MongoAssignmentRepository(IAssignmentRepository):
    """Реализация репозитория заданий (из crud.py)"""
    async def get_by_id(self, assignment_id: str) -> Optional[Dict[str, Any]]:
        try:
            assignment = db.assignments.find_one({"_id": ObjectId(assignment_id)})
            return _assignment_serializer(assignment)
        except Exception:
            return None

    async def get_all_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        return [_assignment_serializer(a) for a in db.assignments.find({"user_id": user_id})]

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = db.assignments.insert_one(data)
        return await self.get_by_id(result.inserted_id)

    async def update(self, assignment_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        db.assignments.update_one({"_id": ObjectId(assignment_id)}, {"$set": data})
        return await self.get_by_id(assignment_id)

    async def delete(self, assignment_id: str) -> bool:
        result = db.assignments.delete_one({"_id": ObjectId(assignment_id)})
        return result.deleted_count > 0

    async def update_status(self, assignment_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        # Эта функция теперь отвечает ТОЛЬКО за обновление БД
        db.assignments.update_one({"_id": ObjectId(assignment_id)}, {"$set": {"status": new_status}})
        return await self.get_by_id(assignment_id)