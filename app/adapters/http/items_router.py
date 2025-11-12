# task-service/app/adapters/http/items_router.py

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.adapters.http.schemas import (
    AssignmentResponseSchema, 
    AssignmentCreateSchema, 
    StatusUpdateSchema
)
from app.usecase.items import AssignmentUseCase

# ИМПОРТЫ ИСПРАВЛЕНЫ
from app.di import get_assignment_usecase
from app.infrastructure.security import get_current_user_id 

router = APIRouter(prefix="/assignments", tags=["Assignments"])

@router.get("", response_model=List[AssignmentResponseSchema])
async def list_assignments(
    user_id: str = Depends(get_current_user_id),
    usecase: AssignmentUseCase = Depends(get_assignment_usecase)
):
    return await usecase.get_all_for_user(user_id)

@router.post("", response_model=AssignmentResponseSchema)
async def create_assignment(
    item: AssignmentCreateSchema,
    user_id: str = Depends(get_current_user_id),
    usecase: AssignmentUseCase = Depends(get_assignment_usecase)
):
    return await usecase.create(item, user_id)

@router.get("/{id}", response_model=AssignmentResponseSchema)
async def get_assignment(
    id: str,
    user_id: str = Depends(get_current_user_id),
    usecase: AssignmentUseCase = Depends(get_assignment_usecase)
):
    result = await usecase.get_by_id(id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result

@router.put("/{id}/status")
async def update_status(
    id: str,
    status_update: StatusUpdateSchema,
    user_id: str = Depends(get_current_user_id),
    usecase: AssignmentUseCase = Depends(get_assignment_usecase)
):
    try:
        updated = await usecase.update_status(id, status_update.status, user_id)
        return {"message": f"Status updated to '{status_update.status}'", "assignment": updated}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{id}")
async def delete_assignment(
    id: str,
    user_id: str = Depends(get_current_user_id),
    usecase: AssignmentUseCase = Depends(get_assignment_usecase)
):
    try:
        await usecase.delete(id, user_id)
        return {"message": "Deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))