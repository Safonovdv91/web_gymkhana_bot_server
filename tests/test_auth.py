from httpx import AsyncClient
from sqlalchemy import insert, select
from src.roles.models import Role
from tests.conftest import client, async_session_maker


class TestApiAuthentification:


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
