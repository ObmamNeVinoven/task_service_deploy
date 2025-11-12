from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def create(self, email: str, hashed_password: str) -> str:
        pass

class IAssignmentRepository(ABC):
    @abstractmethod
    async def get_all_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_by_id(self, assignment_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def update(self, assignment_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def delete(self, assignment_id: str) -> bool:
        pass

    @abstractmethod
    async def update_status(self, assignment_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        pass