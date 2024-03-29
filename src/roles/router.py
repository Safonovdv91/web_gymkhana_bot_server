from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger.logger import logger
from src.database import get_async_session

from ..auth.auth_config import current_user
from ..users.models import User
from .dependecies import role_by_id, role_by_name
from .schemas import (
    Role,
    RoleCreate,
    RoleResponseMany,
    RoleResponseOne,
    RoleUpdatePartial,
)
from .service import RoleService


router_role = APIRouter(prefix="/api/v1/roles", tags=["role"])


@router_role.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    description="Adding new role to DB",
    summary="Additing new user role",
    responses={
        status.HTTP_201_CREATED: {
            "model": RoleResponseOne,  # custom pydantic model for 201 response
            "description": "Creates role from user request ",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,  # custom pydantic model for 401 response
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,  # custom pydantic model for 401 response
            "description": "Not valid data for new role",
        },
        # status.HTTP_202_ACCEPTED: {
        #     "model": AcceptedResponse,  # custom pydantic model for 202 response
        #     "description": "Accepts request and handles it later",
        # },
    },
)
async def add_role(
    new_role: RoleCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(
        f"[ROLE][POST][{user.email}]: try add new role: {new_role.name} - {new_role.description}"
    )
    role = await RoleService.add_new_role(session, new_role, current_user=user)
    return {
        "status": "Success",
        "data": role,
        "details": f"Adding role: [{role.name} - {role.description}] SUCCESS",
    }


@router_role.get(
    "",
    responses={
        status.HTTP_200_OK: {
            "model": RoleResponseMany,  # custom pydantic model for 201 response
            "description": "Returm all existing roles",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,  # custom pydantic model for 401 response
            "description": "UNAUTHORIZED",
        },
    },
)
async def get_roles(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(f"[ROLE][GET][{user.email}]: get all roles.")
    result = await RoleService.get_roles(session=session, current_user=user)
    return {
        "status": "Success",
        "data": result,
        "details": {"count_roles": len(result)},
    }


@router_role.get(
    "/id={role_id}",
    responses={
        status.HTTP_200_OK: {
            "model": RoleResponseOne,  # custom pydantic model for 201 response
            "description": "Return 1 role, by id",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,  # custom pydantic model for 401 response
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,  # custom pydantic model for 401 response
            "description": "Not valid id, must be int",
        },
    },
)
async def get_role_by_id(
    user: User = Depends(current_user),
    role: Role = Depends(role_by_id),
):
    logger.info(
        f"[ROLE][GET][{user.email}]: get role_by id | id:[{role.id}] - {role.name}."
    )
    return {"status": "Success", "data": role, "details": None}


@router_role.get(
    "/name={role_name}",
    responses={
        status.HTTP_200_OK: {
            "model": RoleResponseOne,
            "description": "Return 1 role, by name",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,
            "description": "Not valid 'name', must be str",
        },
    },
)
async def get_role_by_name(
    user: User = Depends(current_user),
    role: Role = Depends(role_by_name),
):
    logger.info(
        f"[ROLE][GET][{user.email}]: get role_by_name | id:[{role.id}] - {role.name}."
    )
    return {"status": "Success", "data": role, "details": None}


@router_role.delete(
    "/id={role_id}/delete",
    responses={
        status.HTTP_200_OK: {
            "model": RoleResponseOne,
            "description": "Role delete success, return deleting role data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,
            "description": "Not valid 'id', must be int",
        },
    },
)
async def delete_role_by_id(
    user: User = Depends(current_user),
    role: Role = Depends(role_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(
        f"[ROLE][DELETE] {user.email} : delete role_by id | id:[{role.id}] - {role.name}."
    )
    result = await RoleService.delete_role(session=session, role=role)
    return {"status": "Success", "data": result, "details": "Was deleted!"}


@router_role.delete(
    "/name={role_name}/delete",
    responses={
        status.HTTP_200_OK: {
            "model": RoleResponseOne,
            "description": "Role delete success, return deleting role data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,
            "description": "Not valid 'name', must be str",
        },
    },
)
async def delete_role_by_name(
    user: User = Depends(current_user),
    role: Role = Depends(role_by_name),
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(
        f"[ROLE][DELETE] {user.email} : delete role_by name | name:[{role.name}]"
    )
    result = await RoleService.delete_role(session=session, role=role)
    return {"status": "Success", "data": result, "details": "Was deleted!"}


@router_role.patch(
    "/id={role_id}/update",
    responses={
        status.HTTP_200_OK: {
            "model": RoleResponseOne,
            "description": "Role patch success, return updating role",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,
            "description": "Not valid data",
        },
    },
)
async def update_role_partial(
    role_update: RoleUpdatePartial,
    user: User = Depends(current_user),
    role: Role = Depends(role_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    logger.info(
        f"[ROLE][PATCH] {user.email} : patch role\n"
        f"old: [{role.id}:{role.name} -[{role.description}]\n"
        f"new: [{role_update.model_dump()}:"
    )

    result = await RoleService.update_role_partial(
        session=session, role=role, role_update=role_update
    )
    return {"status": "Success", "data": result, "details": "Update success"}
