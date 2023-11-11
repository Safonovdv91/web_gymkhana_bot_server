from fastapi import HTTPException
from fastapi_users.schemas import model_dump
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.users.models import Role, User
from src.users.schemas import RoleCreate


class UserRepository:
    @classmethod
    async def get_users(
        cls,
        session: AsyncSession,
        # user: User = Depends(current_user),
    ):
        query = select(User).options(selectinload(User.role))
        users = await session.execute(query)

        return users

    @classmethod
    async def get_user_by_id(
        cls,
        session: AsyncSession,
        user_id: int,
    ):
        query = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
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

    @classmethod
    async def get_user_by_email(
        cls,
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

    @classmethod
    async def delete_user_by_email(
        cls,
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

    @classmethod
    async def delete_user_by_id(
        cls,
        session: AsyncSession,
        user_id: int,
    ):
        query = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
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


class RoleRepository:
    @classmethod
    async def add_new_role(self, session: AsyncSession, new_role: RoleCreate):
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
