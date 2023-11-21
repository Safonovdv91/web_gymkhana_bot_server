from fastapi import HTTPException
from fastapi_users.schemas import model_dump
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
    spoert_classes = result.scalars().all()
    return list(spoert_classes)


async def get_users(session: AsyncSession, sport_class: str):
    query = (
        select(SportClass)
        .where(SportClass.sport_class == sport_class)
        .options(selectinload(SportClass.users))
    )
    result = await session.execute(query)
    sport_class = result.scalar()
    return sport_class
