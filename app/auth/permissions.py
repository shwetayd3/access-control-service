from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.models.user_role import UserRole
from app.models.role import Role
from app.auth.dependencies import get_current_user


def require_role(required_role: str):
    """
    Dependency factory to enforce RBAC.
    Usage:
        @router.get("/admin")
        async def admin_route(
            user: User = Depends(require_role("admin"))
        ):
            ...
    """

    async def role_checker(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ):
        # Query user's roles
        stmt = (
            select(Role.name)
            .join(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.user_id == current_user.id)
        )

        result = await db.execute(stmt)
        roles = result.scalars().all()

        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return current_user

    return role_checker
