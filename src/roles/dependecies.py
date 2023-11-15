from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.roles.models import Role
from src.roles.service import RoleService


async def role_by_id(
    role_id: Annotated[int, Path],
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
) -> Role:
    role = await RoleService.get_role_by_id(session=session, role_id=role_id)

    if role is None:
        raise HTTPException(
            status_code=404, detail=f"Role id={role_id} not found!"
        )
    return role
