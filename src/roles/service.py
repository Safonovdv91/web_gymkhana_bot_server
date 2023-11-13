from sqlalchemy.ext.asyncio import AsyncSession

from src.roles.crud import RoleRepository
from src.roles.models import Role


class RoleService:
    @classmethod
    async def add_new_role(
        cls,
        session: AsyncSession,
        new_role,
    ):
        role: Role = await RoleRepository.add_new_role(session, new_role)

        return cls.role_to_dict(role)

    @classmethod
    def role_to_dict(cls, role: Role):
        output = {
            "role": role.name,
            "description": role.description,
        }
        return output
