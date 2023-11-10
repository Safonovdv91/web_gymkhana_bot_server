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
        stmt = select(User).options(selectinload(User.role))
        result = await session.execute(stmt)
        users = []
        for row in result.scalars():
            user = row
            users.append(
                {
                    "id": user.id,
                    "login": user.login,
                    "email": user.email,
                    "sub_ggp_percent": user.sub_ggp_percent,
                    "ggp_percent_begin": user.ggp_percent_begin,
                    "ggp_percent_end": user.ggp_percent_end,
                    "sub_offline": user.sub_offline,
                    "sub_ggp": user.sub_ggp,
                    "sub_world_record": user.sub_world_record,
                    "registered_at": user.registered_at,
                    "telegram_id": user.telegram_id,
                    "role": user.role.name,
                }
            )

        return users
