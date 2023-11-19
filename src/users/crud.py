from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import User


async def get_user_by_mask(
    session: AsyncSession, mask=None, mask_name: str | bool | int = None
) -> User | None | list[User]:
    query = (
        select(User)
        .options(selectinload(User.role))
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
