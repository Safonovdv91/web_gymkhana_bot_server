from fastapi import APIRouter, Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.schemas import OkResponse
from src.users.models import Role
from src.users.schemas import CreatedResponse, RoleCreate
from src.users.service import RoleService


router_role = APIRouter(prefix="/api/v1/roles", tags=["role"])


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
    role = await RoleService.add_new_role(session, new_role)

    return {
        "status": "Success",
        "data": role,
        "details": "Additing role success",
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
