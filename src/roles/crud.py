from fastapi import HTTPException
from fastapi_users.schemas import model_dump
from sqlalchemy import Result, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from logger.logger import logger
from .models import Role
from .schemas import RoleCreate, RoleUpdate, RoleUpdatePartial


async def add_new_role(session: AsyncSession, new_role: RoleCreate):
    try:
        stmt = insert(Role).values(**model_dump(new_role))
        await session.execute(stmt)
        await session.commit()
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database Exc: "
        else:
            msg = "Unknown Exc: "
        msg += "Can not add new role"
        extra = {"role_mame": new_role.name, "role_description": new_role.description}

        logger.error(msg=msg, extra=extra, exc_info=True)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Error",
                "data": model_dump(new_role),
                "details": f"Error {e}",
            },
        )
    return new_role


async def get_roles(session: AsyncSession) -> list[Role]:
    try:
        query = select(Role).order_by(Role.id)
        result: Result = await session.execute(query)
        roles = result.scalars().all()
        list_roles = list(roles)
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database Exc: "
        else:
            msg = "Unknown Exc: "
        msg += "Can not add new role"

        logger.error(msg=msg, exc_info=True)
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Error",
                "data": list_roles,
                "details": f"Error {e}",
            },
        )
    return list_roles


async def get_role_by_id(session: AsyncSession, role_id: int) -> Role | None:
    return await session.get(Role, role_id)


async def get_role_by_mask(
    session: AsyncSession,
    mask,
    mask_name: str,
) -> Role | None:
    """
    Осуществляет поиск роли по маске
    """
    query = select(Role).where(mask == mask_name)
    result: Result = await session.execute(query)
    role = result.scalar_one_or_none()
    return role


async def create_role(session: AsyncSession, role_in: RoleCreate) -> Role:
    role = Role(**role_in.model_dump())
    session.add(role)
    await session.commit()
    # await session.refresh(role)
    return role


async def update_role(
    session: AsyncSession,
    role: Role,
    role_update: RoleUpdate | RoleUpdatePartial,
    partial: bool = False,
) -> Role:
    for name, value in role_update.model_dump(exclude_unset=partial).items():
        setattr(role, name, value)
    await session.commit()
    return role


async def delete_role(session: AsyncSession, role: Role) -> Role | None:
    await session.delete(role)
    await session.commit()
    return role
