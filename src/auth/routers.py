from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.schemas import model_dump
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.auth_config import current_user
from src.auth.models import Role, User
from src.auth.schemas import RoleCreate
from src.database import get_async_session


fake_user = [{"user1": 1}, {"user2": 2}]
router = APIRouter(prefix="/user", tags=["user"])

router_role = APIRouter(prefix="/role", tags=["user", "role"])


@router.get("/get")
async def get_users(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    stmt = select(User).options(selectinload(User.role))
    result = await session.execute(stmt)
    users = []
    for row in result.scalars():
        user = row
        users.append({"name": user.id, "role": user.role.name})

    return {"status": "success", "data": users, "details": None}


@router_role.post("/role")
async def add_role(
    new_role: RoleCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = insert(Role).values(**model_dump(new_role))
        await session.execute(stmt)
        await session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500)
    return {"status": "success", "data": new_role, "details": None}


@router_role.get("/role")
async def get_roles(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Role)
    roles = []
    for role in await session.scalars(stmt):
        roles.append(role)
    result = roles
    return {"status": "success", "data": result, "details": None}


@router_role.get("/roles/{role_id}")
async def get_role(
    role_id: str, session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Role).where(Role.id == int(role_id))
    result = await session.scalar(stmt)
    return {"status": "success", "data": result, "details": None}


@router_role.delete("/role/{role_id}")
async def delete_role(
    role_id, session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(Role).where(Role.id == int(role_id))
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", "data": role_id, "details": "Was deleted!"}
