from sqlalchemy.ext.asyncio import AsyncSession

from ...mongo_db import student_collection
from ..models import User


class MongoCRUD:
    @staticmethod
    async def get_users_by_mask(
        mask=None, mask_name: str | bool | int | None = None
    ) -> None | list[User]:
        users = await student_collection.find().to_list(1000)
        return users
