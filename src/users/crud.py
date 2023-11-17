from fastapi import HTTPException
from sqlalchemy import Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.roles.models import Role
from src.users.models import User


async def get_users(
    session: AsyncSession,
    # user: User = Depends(current_user),
):
    query = select(User).options(selectinload(User.role))
    users = await session.execute(query)

    return users


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
):
    query = (
        select(User).options(selectinload(User.role)).where(User.id == user_id)
    )
    # result: Result = await session.execute(query)
    # user: User | None = result.scalar_one_or_none()
    user = await session.scalar(query)  # Сокращение кода
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "Not exist",
                "data": None,
                "details": "Sorry, but you was deleted",
            },
        )
    return user


async def get_user_by_email(
    session: AsyncSession,
    email: str,
):
    query = (
        select(User)
        .options(selectinload(User.role))
        .where(User.email == email)
    )
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "Not exist",
                "data": email,
                "details": f"User with email={email} not exist",
            },
        )
    return user


async def get_users_by_role(
    session: AsyncSession, role_id: int
) -> list[Role] | None:
    query = (
        select(User).options(selectinload(User.role)).where(Role.id == role_id)
    )
    result: Result = await session.execute(query)
    users = list(result.scalars().all())
    return users


async def delete_user_by_email(
    session: AsyncSession,
    email: str,
):
    query = (
        select(User)
        .options(selectinload(User.role))
        .where(User.email == email)
    )
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "Success",
                "data": email,
                "details": f"User email={email} not exist",
            },
        )
    stmt = delete(User).where(User.email == email)
    await session.execute(stmt)
    await session.commit()
    return user


async def delete_user_by_id(
    session: AsyncSession,
    user_id: int,
):
    query = (
        select(User).options(selectinload(User.role)).where(User.id == user_id)
    )
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "Success",
                "data": None,
                "details": f"User id={user_id} not exist",
            },
        )
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()
    return user
