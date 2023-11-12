from httpx import AsyncClient
from sqlalchemy import insert, select
from src.users.models import Role
from tests.conftest import client, async_session_maker


class TestApiAuthentification:
    async def test_add_role(
        self,
    ):
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

    def test_register_post(
        self,
    ):
        response = client.post(
            url="/auth/register",
            json={
                "email": "user3@example.com",
                "password": "string",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "login": "string",
            },
        )

        assert response.status_code == 201, "User not add"
        response = client.post(
            url="/auth/register",
            json={
                "email": "for_login@example.com",
                "password": "string",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "login": "string",
            },
        )
        assert response.status_code == 201, "For login user not add"

    def test_register_post_duplicate(
        self,
    ):
        response = client.post(
            url="/auth/register",
            json={
                "email": "user3@example.com",
                "password": "string",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "login": "string",
            },
        )

        assert response.status_code == 400, "Duplicat was added"

    def test_register_post_not_all_data(
        self,
    ):
        response = client.post(
            url="/auth/register",
            json={
                "email": "user_valid@example.com",
                "password": "string",
                "login": "Loh",
            },
        )
        assert response.status_code == 201, "Duplicat was added"

    async def test_register_get_not_all_data(self, ac: AsyncClient):
        response = await ac.get("/api/v1/users/id=2")
        assert (
            response.json()["data"]["email"] == "for_login@example.com"
        ), "User is not valid"

    async def test_login_ok(self, ac: AsyncClient):
        login_url = "/auth/jwt/login"  # Замените на реальный URL
        test_username = "for_login@example.com"
        test_password = "string"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "",
            "username": f"{test_username}",
            "password": f"{test_password}",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        response = await ac.post(login_url, headers=headers, data=data)
        assert response.status_code == 204
