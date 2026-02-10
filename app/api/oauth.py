from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/oauth", tags=["OAuth"])

async def verify_google_token(token: str) -> dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": token},
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    data = resp.json()

    if data["aud"] != settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Invalid token audience")

    return data

@router.post("/google")
async def google_login(token: str, db: AsyncSession = Depends(get_db)):
    data = await verify_google_token(token)

    email = data["email"]

    user = await db.execute(
        select(User).where(User.email == email)
    )
    user = user.scalar_one_or_none()

    if not user:
        user = User(
            email=email,
            is_active=True,
            is_oauth=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access_token = create_access_token({"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
