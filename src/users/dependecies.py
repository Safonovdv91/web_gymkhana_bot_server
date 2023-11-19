from typing import Annotated

from fastapi import Depends, HTTPException, Path
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from .models import User
from .service import UserService


async def user_by_id(
    user_id: Annotated[int, Path(ge=1, le=1_000_000)],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    user = await UserService.get_user_by_id(session=session, user_id=user_id)

    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User id={user_id} not found!"
        )
    return user


async def user_by_email(
    email: Annotated[EmailStr, Path],
    session: AsyncSession = Depends(get_async_session),
) -> User:
    user = await UserService.get_user_by_email(session=session, email=email)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User email={email} not found!"
        )
    return user
