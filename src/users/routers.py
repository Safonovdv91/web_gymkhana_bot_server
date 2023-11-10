from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.schemas import model_dump
from pydantic import EmailStr
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.auth_config import current_user
from src.database import get_async_session
from src.schemas import OkResponse
from src.users.models import Role, User
from src.users.schemas import CreatedResponse, RoleCreate
from src.users.service import UserService


router = APIRouter(prefix="/api/v1/users", tags=["user"])
router_role = APIRouter(prefix="/api/v1/roles", tags=["role"])


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,  # custom pydantic model for 200 response
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


@router.get("/id={user_id}")
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    user = await UserService.get_user_by_id(session, user_id)

    return {"status": "Success", "data": user, "details": None}


@router.get("/current")
async def get_current_user(
    session: AsyncSession = Depends(get_async_session),
    curr_user: User = Depends(current_user),
):
    user = await UserService.get_user_by_id(session, int(curr_user.id))
    return {"status": "Success", "data": user, "details": None}


@router.get(
    "/get/email={email}",
)
async def get_user_email(
    email: EmailStr, session: AsyncSession = Depends(get_async_session)
):
    user = await UserService.get_user_by_email(session, email)

    return {"status": "Success", "data": user, "details": None}


@router.delete(
    "/delete/email={email}",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,  # custom pydantic model for 200 response
            "description": "Deleting user by id",
        },
    },
)
async def del_user_email(
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
    "/delete/id={user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,  # custom pydantic model for 200 response
            "description": "Deleting user by id",
        },
    },
)
async def del_user_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    user = await UserService.delete_user_by_id(session, user_id)

    return {"status": "Success", "data": user, "details": "Was deleted"}


@router_role.post(
    "/add",
    # response_model=**,
    status_code=status.HTTP_201_CREATED,
    description="Adding new role to DB",
    tags=["create"],
    summary="Additing new user role",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,  # custom pydantic model for 200 response
            "description": "Ok Response",
        },
        status.HTTP_201_CREATED: {
            "model": CreatedResponse,  # custom pydantic model for 201 response
            "description": "Creates role from user request ",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": CreatedResponse,  # custom pydantic model for 401 response
            "description": "UNAUTHORIZED",
        },
        # status.HTTP_202_ACCEPTED: {
        #     "model": AcceptedResponse,  # custom pydantic model for 202 response
        #     "description": "Accepts request and handles it later",
        # },
    },
)
async def add_role(
    new_role: RoleCreate,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    try:
        stmt = insert(Role).values(**model_dump(new_role))
        await session.execute(stmt)
        await session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail={
                "status": "Success",
                "data": model_dump(new_role),
                "details": "some information about error",
            },
        )
    return {
        "status": "Success",
        "data": new_role,
        "details": "add role",
    }


@router_role.get("/get")
async def get_roles(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Role)
    roles = []
    for role in await session.scalars(stmt):
        roles.append(role)
    result = roles
    return {"status": "Success", "data": result, "details": None}


@router_role.get("/get/{role_id}")
async def get_role(
    role_id: str, session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Role).where(Role.id == int(role_id))
    result = await session.scalar(stmt)
    return {"status": "Success", "data": result, "details": None}


@router_role.delete("/del/{role_id}")
async def delete_role(
    role_id, session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(Role).where(Role.id == int(role_id))
    await session.execute(stmt)
    await session.commit()
    return {"status": "Success", "data": role_id, "details": "Was deleted!"}
