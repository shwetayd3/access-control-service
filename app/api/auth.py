from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.auth.passwords import verify_password
from app.auth.jwt import create_access_token
from app.schemas.user import UserCreate,UserLogin,UserResponse
from app.core.security import get_password_hash

#router = APIRouter(prefix="/auth", tags=["auth"])
router = APIRouter()


@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"message": "User registered successfully"}