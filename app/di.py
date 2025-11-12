# task-service/app/di.py

from functools import lru_cache
from fastapi import Depends
from app.domain.repositories import IUserRepository, IAssignmentRepository
from app.adapters.repo.mongo_item_repo import MongoUserRepository, MongoAssignmentRepository
from app.usecase.items import AuthUseCase, AssignmentUseCase

@lru_cache(maxsize=1)
def get_user_repo() -> IUserRepository:
    return MongoUserRepository()

@lru_cache(maxsize=1)
def get_assignment_repo() -> IAssignmentRepository:
    return MongoAssignmentRepository()

def get_auth_usecase(
    user_repo: IUserRepository = Depends(get_user_repo)
) -> AuthUseCase:
    return AuthUseCase(user_repo=user_repo)

def get_assignment_usecase(
    assignment_repo: IAssignmentRepository = Depends(get_assignment_repo)
) -> AssignmentUseCase:
    return AssignmentUseCase(assignment_repo=assignment_repo)