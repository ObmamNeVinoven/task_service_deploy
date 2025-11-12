from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.adapters.http.schemas import UserCreateSchema, TokenResponseSchema
from app.usecase.items import AuthUseCase
from app.di import get_auth_usecase # DI

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=TokenResponseSchema)
async def signup(
    user: UserCreateSchema,
    usecase: AuthUseCase = Depends(get_auth_usecase)
):
    try:
        return await usecase.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponseSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUseCase = Depends(get_auth_usecase)
):
    try:
        return await usecase.login(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))