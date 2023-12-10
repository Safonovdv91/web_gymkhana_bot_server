from fastapi import HTTPException
from fastapi_users.schemas import model_dump
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from logger.logger import logger
from src.sport_classes.models import SportClass
from src.sport_classes.schemas import SportClassSchema


async def add_new_sport_class(
    session: AsyncSession, new_class: SportClassSchema
):
    try:
        stmt = insert(SportClass).values(**model_dump(new_class))
        await session.execute(stmt)
        await session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Error",
                "data": model_dump(new_class),
                "details": f"Error {e}",
            },
        )
    return new_class


async def get_sport_classes(session: AsyncSession) -> list[SportClass]:
    query = select(SportClass).order_by(SportClass.id)
    result = await session.execute(query)
    sport_classes = result.scalars().all()
    return list(sport_classes)


async def get_sport_class_by_name(
    session: AsyncSession, name: str
) -> list[SportClass]:
    try:
        logger.debug("Get sportclass by name")
        query = select(SportClass).where(SportClass.sport_class == name)
        result = await session.execute(query)
        sport_class = result.scalar()
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database Exc: "
        else:
            msg = "Unknown Exc: "
        msg += "Can not get sport class by name"
        extra = {
            "name": name,
        }
        logger.error(msg=msg, extra=extra, exc_info=True)

    return sport_class


async def get_users(session: AsyncSession, sport_class: str):
    query = (
        select(SportClass)
        .where(SportClass.sport_class == sport_class)
        .options(selectinload(SportClass.users))
    )
    result = await session.execute(query)
    sport_class = result.scalar()
    return sport_class
