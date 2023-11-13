from fastapi import HTTPException
from fastapi_users.schemas import model_dump
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.roles.models import Role
from src.roles.schemas import RoleCreate


class RoleRepository:
    @classmethod
    async def add_new_role(cls, session: AsyncSession, new_role: RoleCreate):
        try:
            stmt = insert(Role).values(**model_dump(new_role))
            await session.execute(stmt)
            await session.commit()
        except Exception:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "Error",
                    "data": model_dump(new_role),
                    "details": "Role already exist in DB",
                },
            )
        return new_role
