from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..sport_classes.models import SportClass
from .models import User


async def get_user_by_mask(
    session: AsyncSession, mask=None, mask_name: str | bool | int = None
) -> User | None | list[User]:
    query = (
        select(User)
        .options(selectinload(User.role))
        .options(selectinload(User.ggp_sub_classes))
        .where(mask == mask_name)
        .order_by(User.id)
    )
    user: User = await session.scalar(query)
    return user


async def get_users_by_mask(
    session: AsyncSession, mask=None, mask_name: str | bool | int = None
) -> None | list[User]:
    query = (
        select(User)
        .options(selectinload(User.role))
        .options(selectinload(User.ggp_sub_classes))
        .where(mask == mask_name)
        .order_by(User.id)
    )
    result = await session.execute(query)
    users = result.scalars().all()
    return list(users)


async def delete_user(
    session: AsyncSession,
    user: User,
) -> User:
    await session.delete(user)
    await session.commit()
    return user


async def subscribe_ggp_class(
    session: AsyncSession, user: User, class_name: str
) -> User:
    query_class = select(SportClass).where(
        SportClass.sport_class == class_name
    )
    sport_class = await session.scalar(query_class)
    query = (
        select(User)
        .where(User.id == user.id)
        .options(selectinload(User.ggp_sub_classes))
        .options(selectinload(User.role))
    )
    user = await session.scalar(query)
    if sport_class in user.ggp_sub_classes:
        user.ggp_sub_classes.remove(sport_class)
    else:
        user.ggp_sub_classes.append(sport_class)
    await session.commit()
    return user
