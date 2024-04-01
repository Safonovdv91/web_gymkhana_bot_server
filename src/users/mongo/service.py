from copy import copy

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from .crud import MongoCRUD as crud
from .schemas import UserModel, UsersCollection, SportClass


class UserService:
    @classmethod
    async def get_users(
        cls,
    ) -> list[User] | None:
        # users: list[User] | None = await crud.get_users_by_mask()
        users = await crud.get_users_by_mask()
        users = deserelize_fx(users)
        return users


def deserelize_fx(users):
    """
    Десериализация пользователя в объект
    """
    new_user_collection = []
    user_collection = UsersCollection(users=users)
    for user in user_collection.users:
        new_user = copy(user)
        new_user.ggp_sub_classes = []
        for each_sub_class in user.ggp_sub_classes:
            sport_class = SportClass(sport_class=each_sub_class, description="Huita")
            new_user.ggp_sub_classes.append(sport_class)
            # new_user.ggp_sub_classes.append({"sport_class": each_sub_class})

        new_user_collection.append(new_user)
    print("____")
    print("____")
    print("____")

    return new_user_collection
