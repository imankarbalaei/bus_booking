from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await auth_service.register_user(user)

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    return await auth_service.login_user(req.phone_number, req.password)

