from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ..roles.models import Role
from ..sport_classes.crud import get_sport_class_by_name
from . import crud
from .models import User


class UserService:
    @classmethod
    async def get_users(
        cls,
        session: AsyncSession,
        user: User | None = None,
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
        user_delete: User = await crud.delete_user(session, user)
        return user_delete

    @staticmethod
    async def user_subscribe_ggp_class(
        session: AsyncSession, user_in: User, class_names: str | List[str]
    ) -> User | None:
        if type(class_names) is str:
            class_names = [class_names]

        for class_name in class_names:
            sport_class = await get_sport_class_by_name(
                session=session, name=class_name
            )
            if sport_class in user_in.ggp_sub_classes:
                user: User = await crud.remove_ggp_class(
                    session=session, user=user_in, sport_class=sport_class
                )
            else:
                user: User = await crud.append_ggp_class(
                    session=session, user=user_in, sport_class=sport_class
                )

            if user:
                return user
            else:
                return None
