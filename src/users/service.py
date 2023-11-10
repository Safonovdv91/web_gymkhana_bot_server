from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.repository import UserRepository


class UserService:

    @classmethod
    async def lst(cls,
            session: AsyncSession = Depends(get_async_session),
            # user: User = Depends(current_user),
    ):
        result = await UserRepository.get_users(session)

        output = []
        for row in result.scalars().all():
            user = row
            output.append(
                {
                    "id": user.id,
                    "login": user.login,
                    "role": user.role.name,
                    "email": user.email,
                    "sub_ggp_percent": user.sub_ggp_percent,
                    "ggp_percent_begin": user.ggp_percent_begin,
                    "ggp_percent_end": user.ggp_percent_end,
                    "sub_offline": user.sub_offline,
                    "sub_ggp": user.sub_ggp,
                    "sub_world_record": user.sub_world_record,
                    "registered_at": user.registered_at,
                    "telegram_id": user.telegram_id,
                }
            )

        return output
