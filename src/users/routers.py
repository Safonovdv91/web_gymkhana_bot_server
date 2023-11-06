from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.schemas import model_dump
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.auth.auth_config import current_user
from src.users.models import Role, User
from src.database import get_async_session
from src.schemas import OkResponse
from src.users.schemas import CreatedResponse, RoleCreate


router = APIRouter(prefix="/users", tags=["user"])
router_role = APIRouter(prefix="/roles", tags=["role"])


@router.get(
    "/get",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,  # custom pydantic model for 200 response
            "description": "Ok Response",
        },
    },
)
async def get_users(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    stmt = select(User).options(selectinload(User.role))
    result = await session.execute(stmt)
    users = []
    for row in result.scalars():
        user = row
        users.append(
            {
                "id": user.id,
                "login": user.login,
                "email": user.email,
                "sub_ggp_percent": user.sub_ggp_percent,
                "ggp_percent_begin": user.ggp_percent_begin,
                "ggp_percent_end": user.ggp_percent_end,
                "sub_offline": user.sub_offline,
                "sub_ggp": user.sub_ggp,
                "sub_world_record": user.sub_world_record,
                "registered_at": user.registered_at,
                "telegram_id": user.telegram_id,
                "role": user.role.name,
            }
        )

    return {"status": "success", "data": users, "details": None}


@router.get("/get/user_id={user_id}")
async def get_user_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "success",
                "data": user_id,
                "details": f"User email={user_id} not exist",
            },
        )
    return {"status": "success", "data": result.__str__(), "details": None}


@router.get("/get/email={email}")
async def get_user_email(
    email: str, session: AsyncSession = Depends(get_async_session)
):
    stmt = select(User).where(User.email == email)
    result = await session.scalar(stmt)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "success",
                "data": email,
                "details": f"User email={email} not exist",
            },
        )
    return {"status": "success", "data": result.__str__(), "details": None}


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
    email: str,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    stmt = select(User).where(User.email == email)
    result = await session.scalar(stmt)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "success",
                "data": email,
                "details": f"User email={email} not exist",
            },
        )
    stmt = delete(User).where(User.email == email)
    await session.execute(stmt)
    await session.commit()

    return {
        "status": "success",
        "data": None,
        "details": f"{email} Was deleted",
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
    stmt = select(User).where(User.id == user_id)
    result = await session.scalar(stmt)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail={
                "status": "success",
                "data": user_id,
                "details": f"User id={user_id} not exist",
            },
        )
    stmt = delete(User).where(User.id == user_id)
    await session.execute(stmt)
    await session.commit()

    return {"status": "success", "data": result, "details": "Was deleted"}


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
    user: User = Depends(current_user),
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
                "status": "success",
                "data": model_dump(new_role),
                "details": "some information about error",
            },
        )
    return {
        "status": "success",
        "data": new_role,
        "details": f"{user.email} add role",
    }


@router_role.get("/get")
async def get_roles(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Role)
    roles = []
    for role in await session.scalars(stmt):
        roles.append(role)
    result = roles
    return {"status": "success", "data": result, "details": None}


@router_role.get("/get/{role_id}")
async def get_role(
    role_id: str, session: AsyncSession = Depends(get_async_session)
):
    stmt = select(Role).where(Role.id == int(role_id))
    result = await session.scalar(stmt)
    return {"status": "success", "data": result, "details": None}


@router_role.delete("/del/{role_id}")
async def delete_role(
    role_id, session: AsyncSession = Depends(get_async_session)
):
    stmt = delete(Role).where(Role.id == int(role_id))
    await session.execute(stmt)
    await session.commit()
    return {"status": "success", "data": role_id, "details": "Was deleted!"}
