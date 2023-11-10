from httpx import AsyncClient
from sqlalchemy import insert, select
from src.users.models import Role
from tests.conftest import client, async_session_maker


class TestApiAuthentification:

    async def test_add_role(self, ):
        async with async_session_maker() as session:
            stmt = insert(Role).values(id=1, name="Admin", description="Test of admin")
            await session.execute(stmt)
            await session.commit()

            query = select(Role)
            result = await session.scalar(query)

            assert result.id == 1, "Проблема с добавлением роли"
            assert result.name == "Admin"
            assert result.description == "Test of admin"

            stmt = insert(Role).values(id=2, name="User", description="Test of user")
            await session.execute(stmt)
            stmt = insert(Role).values(id=3, name="Guest", description="Test of guest")
            await session.execute(stmt)
            await session.commit()

    def test_register_post(self, ):
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

    def test_register_post_duplicate(self, ):
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

        assert response.status_code == 400, "Duplicat was added"

    def test_register_post_not_all_data(self, ):
        response = client.post(
            url="/auth/register",
            json={
                "email": "user_valid@example.com",
                "password": "string",
                "login": "Loh"
            }
        )
        assert response.status_code == 201, "Duplicat was added"

    async def test_register_get_not_all_data(self, ac: AsyncClient):
        response = await ac.get("/api/v1/users/id=2")
        assert response.json()["data"]["email"] == "user_valid@example.com", "User is not valid"
