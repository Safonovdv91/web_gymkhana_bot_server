from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session
from src.roles.schemas import CreatedResponse, RoleCreate, RoleResponseMany
from src.schemas import OkResponse

from ..auth.auth_config import current_user
from ..users.models import User
from .schemas import RoleResponseOne
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
        "details": "Additing role success",
    }


@router_role.get("/get", response_model=RoleResponseMany)
async def get_roles(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    result = await RoleService.get_roles(session)
    return {"status": "Success", "data": result, "details": None}


@router_role.get("/get/id={role_id}", response_model=RoleResponseOne)
async def get_role_by_id(
    role_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    result = await RoleService.get_role_by_id(session=session, role_id=role_id)

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Role id={role_id} not found!"
        )
    return {"status": "Success", "data": result, "details": None}


@router_role.get("/get/name={role_name}", response_model=RoleResponseOne)
async def get_role_by_name(
    role_name: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    result = await RoleService.get_role_by_name(
        session=session, role_name=role_name
    )

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Role name: {role_name} not found!"
        )
    return {"status": "Success", "data": result, "details": None}


@router_role.delete("/del/{role_id}")
async def delete_role(
    role_id, session: AsyncSession = Depends(get_async_session)
):
    return {"status": "Success", "data": role_id, "details": "Was deleted!"}
