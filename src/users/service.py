from sqlalchemy.ext.asyncio import AsyncSession

from src.users.crud import RoleRepository, UserRepository
from src.users.models import Role, User


class UserService:
    @classmethod
    async def lst(
        cls,
        session: AsyncSession,
        # user: User = Depends(current_user),
    ):
        result = await UserRepository.get_users(session)
        output = []
        for row in result.scalars().all():
            user = row
            user = cls.user_to_dict(user)
            output.append(user)
        return output

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int):
        user: User = await UserRepository.get_user_by_id(session, user_id)

        return cls.user_to_dict(user)

    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str):
        user: User | None = await UserRepository.get_user_by_email(
            session, email
        )

        return cls.user_to_dict(user)

    @classmethod
    async def delete_user_by_email(cls, session: AsyncSession, email: str):
        user: User = await UserRepository.delete_user_by_email(session, email)

        return cls.user_to_dict(user)

    @classmethod
    async def delete_user_by_id(cls, session: AsyncSession, user_id: int):
        user: User = await UserRepository.delete_user_by_id(session, user_id)

        return cls.user_to_dict(user)

    @classmethod
    def user_to_dict(cls, user: User):
        output = {
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
        return output


class RoleService:
    @classmethod
    async def add_new_role(
        cls,
        session: AsyncSession,
        new_role,
    ):
        role: Role = await RoleRepository.add_new_role(session, new_role)

        return cls.role_to_dict(role)

    @classmethod
    def role_to_dict(cls, role: Role):
        output = {
            "role": role.name,
            "description": role.description,
        }
        return output
