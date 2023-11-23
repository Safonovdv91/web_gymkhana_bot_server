from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import current_user
from src.database import get_async_session
from src.sport_classes.schemas import SportClassResponseMany, SportClassSchema

from ..users.models import User
from .crud import add_new_sport_class, get_sport_classes, get_users


router = APIRouter(prefix="/api/v1/sport_classes", tags=["Sport Class"])


@router.post("/")
async def add_sport_class(
    sport_class: SportClassSchema,
    curr_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    sport_class = await add_new_sport_class(session, sport_class)
    return {"status": "Success", "data": sport_class, "details": None}


@router.get("/", response_model=SportClassResponseMany)
async def router_get_sport_classes2(
    # curr_user: Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    sport_class = await get_sport_classes(session)
    return {"status": "Success", "data": sport_class, "details": None}


@router.get("get_users/class={sport_class}")
async def router_get_sport_classes(
    sport_class: str,
    curr_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    sport_class = await get_users(session, sport_class)
    return {"status": "Success", "data": sport_class, "details": None}
