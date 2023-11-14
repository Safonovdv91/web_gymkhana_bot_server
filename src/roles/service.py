from sqlalchemy.ext.asyncio import AsyncSession

from src.roles.models import Role

from ..users.models import User
from . import crud


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
        result = await crud.get_role_by_id(session=session, role_id=role_id)
        return result

    @classmethod
    async def get_role_by_name(
        cls, session: AsyncSession, role_name: str
    ) -> Role:
        result = await crud.get_role_by_name(
            session=session, role_name=role_name
        )
        return result

    @classmethod
    async def delete_role_by_id(
        cls, session: AsyncSession, role_id: int
    ) -> Role:
        result: Role = await crud.delete_role_by_id(session, role_id=role_id)
        print(f"{result.name} was deleted")
        return result
