from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.schemas.role import RoleCreate, RoleResponse
from app.auth.permissions import require_role

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("admin")),
):
    existing = await db.execute(
        select(Role).where(Role.name == role_data.name)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Role already exists")

    role = Role(name=role_data.name)
    db.add(role)
    await db.commit()
    await db.refresh(role)

    return role

@router.get("/", response_model=list[RoleResponse])
async def list_roles(
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("admin")),
):
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.post("/assign")
async def assign_role(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("admin")),
):
    user_obj = await db.get(User, user_id)
    role_obj = await db.get(Role, role_id)

    if not user_obj or not role_obj:
        raise HTTPException(status_code=404, detail="User or Role not found")

    existing = await db.execute(
        select(UserRole)
        .where(UserRole.user_id == user_id)
        .where(UserRole.role_id == role_id)
    )

    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Role already assigned")

    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    await db.commit()

    return {"message": "Role assigned successfully"}

@router.delete("/remove")
async def remove_role(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(require_role("admin")),
):
    result = await db.execute(
        select(UserRole)
        .where(UserRole.user_id == user_id)
        .where(UserRole.role_id == role_id)
    )

    user_role = result.scalar_one_or_none()

    if not user_role:
        raise HTTPException(status_code=404, detail="Assignment not found")

    await db.delete(user_role)
    await db.commit()

    return {"message": "Role removed successfully"}
