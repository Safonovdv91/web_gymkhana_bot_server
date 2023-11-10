from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.users.models import User


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
        result: Result = await session.execute(query)
        user: User | None = result.scalar_one_or_none()
        print(f"Found user {user}")
        return user
