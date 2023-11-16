from sqlalchemy.ext.asyncio import AsyncSession

from src.roles.models import Role

from ..users.models import User
from . import crud
from .schemas import RoleUpdate, RoleUpdatePartial


class RoleService:
    @classmethod
    async def add_new_role(
        cls, session: AsyncSession, new_role, current_user: User
    ) -> Role:
        role: Role = await crud.add_new_role(session, new_role)
        print(f"{current_user.email} add new role: {role}")
        return role

    @classmethod
    async def get_roles(cls, session: AsyncSession) -> list[Role]:
        result: list[Role] = await crud.get_roles(session)
        return result

    @classmethod
    async def get_role_by_id(cls, session: AsyncSession, role_id: int) -> Role:
        return await crud.get_role_by_id(session=session, role_id=role_id)

    @classmethod
    async def get_role_by_name(
        cls, session: AsyncSession, role_name: str
    ) -> Role:
        result = await crud.get_role_by_mask(
            session=session, mask=Role.name, mask_name=role_name
        )
        return result

    @classmethod
    async def delete_role_by_id(
        cls, session: AsyncSession, role: Role
    ) -> Role:
        result: Role = await crud.delete_role(session, role=role)
        print(f"{result.name} was deleted")
        return result

    @classmethod
    async def update_role(
        cls, session: AsyncSession, role: Role, role_update: RoleUpdate
    ):
        return await crud.update_role(
            session=session, role=role, role_update=role_update
        )

    @classmethod
    async def update_role_partial(
        cls, session: AsyncSession, role: Role, role_update: RoleUpdatePartial
    ):
        return await crud.update_role(
            session=session, role=role, role_update=role_update, partial=True
        )
