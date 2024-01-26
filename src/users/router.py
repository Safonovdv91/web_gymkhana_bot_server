from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger.logger import init_logger
from src.auth.auth_config import current_user
from src.database import get_async_session

from ..sport_classes.schemas import SportClassSchemaInput
from .dependencies import user_by_email, user_by_id
from .models import User
from .schemas import (
    SUserResponseOne,
    SUserSearchArgs,
    SUsersResponseMany,
    UserInParticul,
)
from .service import UserService


main_logger = init_logger("src.users.router")

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
    # curr_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    # main_logger.info(f"[USER][GET] user: {curr_user.email} get users")
    users = await UserService.get_users(session=session)
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
):
    # main_logger.info(
    #     f"[USER][GET] user: {curr_user.email} get users [ALL INFO]"
    # )
    users = await UserService.get_users(
        session=session,
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
    # curr_user: User = Depends(current_user),
    user: User = Depends(user_by_id),
):
    # main_logger.info(
    #     f"[USER][GET] user: {curr_user.email} get user by id [{user.id}] - {user.email}"
    # )
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
    main_logger.info(f"[USER][GET] current user: {curr_user.email}")
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
    main_logger.info(
        f"[USER][GET] user: {curr_user.email} get user by email: [{user.email}]"
    )

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
    main_logger.info(
        f"[USER][GET] user: {curr_user.email} get user by role id = {role_id}"
    )
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
    curr_user: User = Depends(current_user),
    user: User = Depends(user_by_email),
    session: AsyncSession = Depends(get_async_session),
):
    main_logger.info(
        f"[USER][DELETE] user: {curr_user.email} DELETE user: {user.email}"
    )
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
    main_logger.info(
        f"[USER][DELETE] user: {curr_user.email} delete user by id {user.id}:{user.email}"
    )
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
    main_logger.info(f"[USER][PATCH] user: {curr_user.email} patch")
    user = await UserService().user_subscribe_ggp_class(
        session=session, user_in=user, class_names=class_name.sport_class
    )
    if user:
        return {
            "status": "Success",
            "data": user,
            "details": f"User with id: [{user.id}] subscribing [{class_name.sport_class}] success!",
        }
    return {
        "status": "User is none",
        "data": user,
        "details": None,
    }


@router.patch(
    "/id={user_id}/patch",
    responses={
        status.HTTP_200_OK: {
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
async def user_patch_by_id(
    #    curr_user: User = Depends(current_user),
    user_update: UserInParticul,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(user_by_id),
):
    # main_logger.info(f"[USER][PATCH] user: {curr_user.email} patch")

    result = await UserService.update_user_partial(
        session=session, user=user, user_update=user_update
    )
    if user:
        return {
            "status": "Success",
            "data": result,
            "details": f"User {user.id} updated success!",
        }
    return {
        "status": "User is none",
        "data": user,
        "details": None,
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
    class_name: SportClassSchemaInput,
    curr_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    main_logger.info(f"[USER][PATCH] current_user: {curr_user.email} patch")

    user = await user_by_id(session=session, user_id=curr_user.id)
    user = await UserService().user_subscribe_ggp_class(
        session=session, user_in=user, class_names=class_name.sport_class
    )
    if user:
        return {
            "status": "Success",
            "data": user,
            "details": f"User with id: [{user.id}] subscribing success!",
        }
    return {
        "status": "User is none",
        "data": user,
        "details": None,
    }
