from httpx import AsyncClient
from sqlalchemy import insert, select

from src.users.models import Role
from tests.conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="test_admin", description="Test of admin")
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.scalar(query)

        assert result.id == 1, "Проблема с добавлением роли"
        assert result.name == "test_admin"
        assert result.description == "Test of admin"

        stmt = insert(Role).values(id=2, name="test_user", description="Test of user")
        await session.execute(stmt)
        await session.commit()


def test_register_post():
    response = client.post(
        url="/auth/register",
        json={
            "email": "user3@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "login": "string"
        }
    )

    assert response.status_code == 201, "User not add"


async def test_register_get(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user5@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "login": "string"
    })
    assert response.status_code == 201, "User add register"


async def test_register_get_(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user5@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "login": "string"
    })
    assert response.status_code == 201, "User add register"
