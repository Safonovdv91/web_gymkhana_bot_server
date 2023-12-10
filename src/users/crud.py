from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from logger.logger import logger

from ..sport_classes.models import SportClass
from .models import User


async def get_user_by_mask(
    session: AsyncSession, mask=None, mask_name: str | bool | int | None = None
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
    session: AsyncSession, mask=None, mask_name: str | bool | int | None = None
) -> None | list[User]:
    try:
        query = (
            select(User)
            .options(selectinload(User.role))
            .options(selectinload(User.ggp_sub_classes))
            .where(mask == mask_name)
            .order_by(User.id)
        )
        result = await session.execute(query)
        users = result.scalars().all()
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database Exc: "
        else:
            msg = "Unknown Exc: "
        msg += "Can not get users by mask"
        extra = {"mask_name": mask_name, "mask": mask}
        logger.error(msg=msg, extra=extra, exc_info=True)
    return list(users)


async def delete_user(
    session: AsyncSession,
    user: User,
) -> User:
    await session.delete(user)
    await session.commit()
    return user


async def append_ggp_class(
    session: AsyncSession, user: User, sport_class: SportClass
) -> User:
    try:
        user.ggp_sub_classes.append(sport_class)
        await session.commit()
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database Exc: "
        else:
            msg = "Unknown Exc: "
        msg += "Can not append ggp_class"
        extra = {"user": user, "sport_class": sport_class}
        logger.error(msg=msg, extra=extra, exc_info=True)

    return user


async def remove_ggp_class(
    session: AsyncSession, user: User, sport_class: SportClass
) -> User:
    try:
        user.ggp_sub_classes.remove(sport_class)
        await session.commit()
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database Exc: "
        else:
            msg = "Unknown Exc: "
        msg += "Can not remove ggp_class"
        extra = {"user": user, "sport_class": sport_class}
        logger.error(msg=msg, extra=extra, exc_info=True)

    return user
