from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.schemas import OkResponse

from ..auth.auth_config import current_user
from ..users.models import User
from .dependecies import role_by_id, role_by_name
from .schemas import (
    CreatedResponse,
    Role,
    RoleCreate,
    RoleResponseMany,
    RoleResponseOne,
    RoleUpdate,
    RoleUpdatePartial,
)
from .service import RoleService


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
    user: User = Depends(current_user),
):
    role = await RoleService.add_new_role(session, new_role, current_user=user)
    return {
        "status": "Success",
        "data": role,
        "details": f"Adding role: [{role.name} - {role.description}] SUCCESS",
    }


@router_role.get("/get", response_model=RoleResponseMany)
async def get_roles(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    result = await RoleService.get_roles(session)
    return {
        "status": "Success",
        "data": result,
        "details": {"count": len(result)},
    }


@router_role.get("/id={role_id}", response_model=RoleResponseOne)
async def get_role_by_id(
    role: Role = Depends(role_by_id),
):
    return {"status": "Success", "data": role, "details": None}


@router_role.get("/name={role_name}", response_model=RoleResponseOne)
async def get_role_by_name(
    role: Role = Depends(role_by_name),
):
    return {"status": "Success", "data": role, "details": None}


@router_role.delete("/id={role_id}/delete")
async def delete_role_id(
    role: Role = Depends(role_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    result = await RoleService.delete_role(session=session, role=role)
    return {"status": "Success", "data": result, "details": "Was deleted!"}


@router_role.delete("/name={role_name}/delete")
async def delete_role_name(
    role: Role = Depends(role_by_name),
    session: AsyncSession = Depends(get_async_session),
):
    result = await RoleService.delete_role(session=session, role=role)
    return {"status": "Success", "data": result, "details": "Was deleted!"}


@router_role.put("/id={role_id}/update")
async def update_role(
    role_update: RoleUpdate,
    role: Role = Depends(role_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    result = await RoleService.update_role(
        session=session, role=role, role_update=role_update
    )
    return {"status": "Success", "data": result, "details": "Update success"}


@router_role.patch("/id={role_id}/update")
async def update_role_partial(
    role_update: RoleUpdatePartial,
    role: Role = Depends(role_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    result = await RoleService.update_role_partial(
        session=session, role=role, role_update=role_update
    )
    return {"status": "Success", "data": result, "details": "Update success"}
