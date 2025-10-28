from app.repositories.user_repo import UserRepository
from app.repositories.wallet_repo import wallet_repo
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_schema import UserCreate
from fastapi import HTTPException, status


async def register_user(user: UserCreate):
    existing = await UserRepository.get_by_phone(user.phone_number)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")

    hashed = hash_password(user.password)
    new_user = await UserRepository.create(user, hashed)
    await wallet_repo.create(new_user["id"], initial_balance=0)
    return dict(new_user)


async def login_user(phone_number: str, password: str):
    user = await UserRepository.get_by_phone(phone_number)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(user["id"])
    return {"access_token": token, "token_type": "bearer"}

