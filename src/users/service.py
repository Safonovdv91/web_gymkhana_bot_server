from sqlalchemy.ext.asyncio import AsyncSession

from ..roles.models import Role
from . import crud
from .models import User


class UserService:
    @classmethod
    async def get_users(
        cls,
        session: AsyncSession,
        user: User = None,
    ) -> list[User] | None:
        users: list[User] | None = await crud.get_users_by_mask(session)
        return users

    @classmethod
    async def get_users_by_role(
        cls, session: AsyncSession, user_role_id: int
    ) -> list[User] | None:
        users: list[User] = await crud.get_users_by_mask(
            session=session, mask=Role.id, mask_name=user_role_id
        )
        return users

    @classmethod
    async def get_user_by_id(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> User:
        user: User = await crud.get_user_by_mask(
            session=session, mask=User.id, mask_name=user_id
        )
        return user

    @classmethod
    async def get_user_by_email(
        cls, session: AsyncSession, email: str
    ) -> User | None:
        user = await crud.get_user_by_mask(
            session=session, mask=User.email, mask_name=email
        )

        return user

    @classmethod
    async def delete_user(cls, session: AsyncSession, user: User) -> User:
        user: User = await crud.delete_user(session, user)
        return user

    @classmethod
    async def user_subscribe_ggp_class(cls, session: AsyncSession, user: User, class_name: str) -> User:
        user: User = await crud.subscribe_ggp_class(session, user, class_name)
        return user
