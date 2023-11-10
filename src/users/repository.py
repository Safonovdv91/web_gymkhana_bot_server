from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database import get_async_session
from src.users.models import User


class UserRepository:
    @classmethod
    async def get_users(cls,
            session: AsyncSession = Depends(get_async_session),
            # user: User = Depends(current_user),
    ):
        query = select(User).options(selectinload(User.role))
        users = await session.execute(query)

        return users

        # return users
