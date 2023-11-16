from typing import Annotated

from fastapi import APIRouter, Depends, Path
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.auth_config import current_user
from src.database import get_async_session
from src.users.models import User
from src.users.schemas import UserResponseMany, UserResponseOne
from src.users.service import UserService


router = APIRouter(prefix="/api/v1/users", tags=["user"])


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseMany,  # custom pydantic model for 200 response
            "description": "Ok Response",
        },
    },
)
async def get_users(
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    data = await UserService.lst(session)
    return {"status": "Success", "data": data, "details": None}


@router.get(
    "/id={user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseOne,  # custom pydantic model for 200 response
            "description": "Deleting user by id",
        },
    },
)
async def get_user_by_id(
    user_id: Annotated[int, Path(ge=1, le=1_000_000)],
    session: AsyncSession = Depends(get_async_session),
):
    user = await UserService.get_user_by_id(session, user_id)

    return {"status": "Success", "data": user, "details": None}


@router.get(
    "/current",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseOne,  # custom pydantic model for 200 response
            "description": "Deleting user by id",
        },
    },
)
async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    curr_user: User = Depends(current_user),
):
    user = await UserService.get_user_by_id(session, int(curr_user.id))
    return {"status": "Success", "data": user, "details": None}


@router.get(
    "/email={email}",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseOne,  # custom pydantic model for 200 response
            "description": "Deleting user by id",
        },
    },
)
async def get_user_by_email(
    email: EmailStr, session: AsyncSession = Depends(get_async_session)
):
    user = await UserService.get_user_by_email(session, email)

    return {"status": "Success", "data": user, "details": None}


@router.get(
    "/role={role}/get",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseMany,  # custom pydantic model for 200 response
            "description": "Ok Response",
        },
    },
)
async def get_users_by_role_id(
    role_id: int, session: AsyncSession = Depends(get_async_session)
):
    users = await UserService.get_users_by_role(
        session=session, user_role_id=role_id
    )

    return {"status": "Success", "data": users, "details": None}


@router.delete(
    "/email={email}/delete",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseOne,  # custom pydantic model for 200 response
            "description": "Deleting user by id",
        },
    },
)
async def del_user_by_email(
    email: EmailStr,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    user = await UserService.delete_user_by_email(session, email)

    return {
        "status": "Success",
        "data": user,
        "details": "Was deleted!",
    }


@router.delete(
    "/id={user_id}/delete",
    responses={
        status.HTTP_200_OK: {
            "model": UserResponseOne,  # custom pydantic model for 200 response
            "description": "Deleting user by id",
        },
    },
)
async def del_user_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    user = await UserService.delete_user_by_id(
        session=session, user_id=user_id
    )

    return {"status": "Success", "data": user, "details": "Was deleted"}
