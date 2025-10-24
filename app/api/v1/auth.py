from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.crud.user_crud import get_user_by_phone, create_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_in: UserCreate):
    existing = await get_user_by_phone(user_in.phone_number)
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    user = await create_user(
        full_name=user_in.full_name,
        phone_number=user_in.phone_number,
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )



    access_token = create_access_token({"user_id": user.id, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(user_in: UserLogin):
    user = await get_user_by_phone(user_in.phone_number)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

