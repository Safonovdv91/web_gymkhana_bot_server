from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    models,
    schemas,
)

from logger.logger import init_logger
from src.auth.utils import get_user_db
from src.config import SECRET_AUTH_MANAGER
from src.users.models import User


SECRET = SECRET_AUTH_MANAGER
logger = init_logger("src.auth.manager")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        функция вынесена для большего понимания и добавления функционала, внизу видно как колонка
        password превращается в колонку hashed password, по этому же принципу для всех новых
        мы можем переорпеделить значение role_id
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict[
            "role_id"
        ] = 3  # переопределение столбца роли для пользователя

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        logger.info(f"User {user.email} has been registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
