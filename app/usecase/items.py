import httpx
from typing import List, Dict, Any
import logging 
from app.domain.repositories import IUserRepository, IAssignmentRepository
from app.settings import settings
from app.adapters.http.schemas import UserCreateSchema, AssignmentCreateSchema

# --- ВОТ ЗДЕСЬ БЫЛА ОШИБКА ---
# Нам нужно импортировать verify_password из auth_utils
from app.infrastructure.auth_utils import (
    hash_password, 
    verify_password,  # <--- ДОБАВЛЕНО
    create_access_token
)

# Setup Logger
log = logging.getLogger(__name__)

class AuthUseCase:
    """Business logic for authentication"""
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo
        self.client = httpx.AsyncClient()

    async def register(self, user_data: UserCreateSchema) -> Dict[str, Any]:
        existing = await self.user_repo.get_by_email(user_data.email)
        if existing:
            raise ValueError("User already exists")
        
        hashed = hash_password(user_data.password) 
        user_id = await self.user_repo.create(user_data.email, hashed)
        
        log.info(f"New user created: {user_id} ({user_data.email})")

        try:
            await self.client.post(f"{settings.PET_SERVICE_URL}/pet-state/create/{user_id}", timeout=5)
            await self.client.post(
                f"{settings.NOTIFICATION_SERVICE_URL}/notifications",
                json={
                    "user_id": user_id,
                    "message": "Welcome! Your account and pet were created.",
                    "type": "system",
                },
                timeout=5,
            )
        except httpx.RequestError as e:
            log.warning(f"Failed to call dependent services for {user_id}: {e}")
            pass 

        token = create_access_token({"sub": user_id})
        return {"access_token": token, "token_type": "bearer"}

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        user = await self.user_repo.get_by_email(email)
        # Теперь verify_password определена и ошибки не будет
        if not user or not verify_password(password, user["password"]):
            raise ValueError("Invalid credentials")
        
        token = create_access_token({"sub": str(user["_id"])})
        return {"access_token": token, "token_type": "bearer"}

class AssignmentUseCase:
    """Business logic for assignments"""
    def __init__(self, assignment_repo: IAssignmentRepository):
        self.repo = assignment_repo
        self.client = httpx.AsyncClient()

    async def get_all_for_user(self, user_id: str):
        return await self.repo.get_all_for_user(user_id)

    async def get_by_id(self, assignment_id: str, user_id: str):
        assignment = await self.repo.get_by_id(assignment_id)
        if not assignment or assignment.get("user_id") != user_id:
            return None
        return assignment

    async def create(self, item: AssignmentCreateSchema, user_id: str):
        data = item.model_dump()
        data["user_id"] = user_id
        new_assignment = await self.repo.create(data)
        
        try:
            await self.client.post(
                f"{settings.NOTIFICATION_SERVICE_URL}/notifications",
                json={
                    "user_id": user_id,
                    "message": f"New assignment: {item.title}",
                    "type": "task",
                },
                timeout=5,
            )
        except httpx.RequestError:
            pass
            
        return new_assignment

    async def update_status(self, assignment_id: str, status: str, user_id: str):
        assignment = await self.repo.get_by_id(assignment_id)
        if not assignment or assignment.get("user_id") != user_id:
            raise ValueError("Not found or permission denied")

        updated = await self.repo.update_status(assignment_id, status)

        try:
            if status.lower() == "completed":
                await self.client.post(f"{settings.PET_SERVICE_URL}/pet-state/increase-mood/{user_id}", timeout=5)
                await self.client.post(f"{settings.NOTIFICATION_SERVICE_URL}/notify/task-completed/{user_id}", timeout=5)
            elif status.lower() == "failed":
                await self.client.post(f"{settings.PET_SERVICE_URL}/pet-state/decrease-health/{user_id}", timeout=5)
                await self.client.post(f"{settings.NOTIFICATION_SERVICE_URL}/notify/task-failed/{user_id}", timeout=5)
        except httpx.RequestError as e:
            log.warning(f"Failed to call dependent services during status update for {user_id}: {e}")
            pass 

        return updated

    async def delete(self, assignment_id: str, user_id: str):
        assignment = await self.repo.get_by_id(assignment_id)
        if not assignment or assignment.get("user_id") != user_id:
            raise ValueError("Not found or permission denied")
        
        return await self.repo.delete(assignment_id)
