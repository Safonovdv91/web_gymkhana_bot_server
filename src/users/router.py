from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.auth_config import current_user
from src.database import get_async_session

from ..sport_classes.schemas import SportClassSchemaInput
from .dependencies import user_by_email, user_by_id
from .models import User
from .schemas import SUserResponseOne, SUserSearchArgs, SUsersResponseMany
from .service import UserService


router = APIRouter(prefix="/api/v1/users", tags=["user"])


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {
            "model": SUsersResponseMany,
            "description": "Return all users in db",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUsersResponseMany,
)
async def get_users(
    curr_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    users = await UserService.get_users(session=session, user=curr_user)
    return {
        "status": "Success",
        "data": users,
        "details": {"count_users": len(users)},
    }


@router.get(
    "/ALL_INFO",
    responses={
        status.HTTP_200_OK: {
            "model": SUsersResponseMany,
            "description": "Return all users in db",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUsersResponseMany,
)
async def get_users_all_info(
    search_args: SUserSearchArgs = Depends(),
    session: AsyncSession = Depends(get_async_session),
    # curr_user: User = Depends(current_user),
) -> SUsersResponseMany:
    users = await UserService.get_users(
        session=session,
        # user=curr_user
    )
    return {
        "status": "Success",
        "data": users,
        "details": {"count_users": len(users)},
    }


@router.get(
    "/id={user_id}",
    responses={
        status.HTTP_200_OK: {
            "model": SUserResponseOne,
            "description": "Return one user data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUserResponseOne,
)
async def get_user_by_id(
    curr_user: User = Depends(current_user),
    user: User = Depends(user_by_id),
):
    return {"status": "Success", "data": user, "details": None}


@router.get(
    "/current",
    responses={
        status.HTTP_200_OK: {
            "model": SUserResponseOne,
            "description": "Return current user data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUserResponseOne,
)
async def get_current_user(
    curr_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user = await UserService.get_user_by_id(
        session=session, user_id=curr_user.id
    )
    return {"status": "Success", "data": user, "details": None}


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": SUserResponseOne,
            "description": "Return one user data by email",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUserResponseOne,
)
async def get_user_by_email(
    curr_user: User = Depends(current_user),
    user: User = Depends(user_by_email),
):
    return {"status": "Success", "data": user, "details": None}


@router.get(
    "/role={role_id}",
    responses={
        status.HTTP_200_OK: {
            "model": SUsersResponseMany,
            "description": "Return all user's data with role",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUsersResponseMany,
)
async def get_users_by_role_id(
    curr_user: User = Depends(current_user),
    role_id: int = 1,
    session: AsyncSession = Depends(get_async_session),
):
    users = await UserService.get_users_by_role(
        session=session, user_role_id=role_id
    )
    return {
        "status": "Success",
        "data": users,
        "details": {"count_users": len(users)},
    }


@router.delete(
    "/email={email}/delete",
    responses={
        status.HTTP_200_OK: {
            "model": SUserResponseOne,
            "description": "Return deleting user data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUserResponseOne,
)
async def del_user_by_email(
    cur_user: User = Depends(current_user),
    user: User = Depends(user_by_email),
    session: AsyncSession = Depends(get_async_session),
):
    user = await UserService.delete_user(session, user)

    return {
        "status": "Success",
        "data": user,
        "details": f"User with email: [{user.email}] delete success!",
    }


@router.delete(
    "/id={user_id}/delete",
    responses={
        status.HTTP_200_OK: {
            "model": SUserResponseOne,
            "description": "Return deleting user data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUserResponseOne,
)
async def del_user_by_id(
    session: AsyncSession = Depends(get_async_session),
    curr_user: User = Depends(current_user),
    user: User = Depends(user_by_id),
):
    user = await UserService.delete_user(session, user)
    return {
        "status": "Success",
        "data": user,
        "details": f"User with email: [{user.id}] delete success!",
    }


@router.patch(
    "/id={user_id}/subscribe",
    responses={
        status.HTTP_201_CREATED: {
            "model": SUserResponseOne,
            "description": "Return deleting user data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUserResponseOne,
)
async def user_subscribe_ggp(
    class_name: SportClassSchemaInput,
    curr_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(user_by_id),
):
    user = await UserService().user_subscribe_ggp_class(
        session=session, user_in=user, class_names=class_name.sport_class
    )
    return {
        "status": "Success",
        "data": user,
        "details": f"User with id: [{user.id}] subscribing [{class_name.sport_class}] success!",
    }


@router.patch(
    "/current/ggp_sub",
    responses={
        status.HTTP_201_CREATED: {
            "model": SUserResponseOne,
            "description": "Return deleting user data",
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": None,
            "description": "UNAUTHORIZED",
        },
    },
    response_model=SUserResponseOne,
)
async def current_user_subscribe_ggp(
    curr_user: User = Depends(current_user),
    class_name: SportClassSchemaInput = -1,
    session: AsyncSession = Depends(get_async_session),
):
    user = await user_by_id(session=session, user_id=curr_user.id)
    user = await UserService().user_subscribe_ggp_class(
        session=session, user_in=user, class_names=class_name.sport_class
    )
    return {
        "status": "Success",
        "data": user,
        "details": f"User with id: [{user.id}] subscribing success!",
    }
