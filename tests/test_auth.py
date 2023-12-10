import json

import pytest
from httpx import AsyncClient


class TestApiAuthentification:
    USERS_REGISTRATION = [
        ("test_user1@test.com", "test_user1", "testpass1", 201),
        ("test_user2@test.com", "test_user2", "testpass2", 201),
        ("test_user3@test.com", "test_user3", "testpass3", 201),
        ("test_user3@test.com", "test_user3", "testpass3", 400),
    ]
    USERS_LOGIN = [
        ("user1@example.com", "string", 204),
        # ("user1@example.com", "not_string", 401),
        ("not_readl@test.com", "testpass2", 400),
        ("@test.com", "testpass3", 400),
        ("test_user3@test.com", "", 422),
        ("", "string", 422),
    ]
    URL_PREFIX = "/auth/register"

    @pytest.mark.parametrize("email, login, password, status_code", USERS_REGISTRATION)
    async def test_registration_new_user(
        self,
        ac: AsyncClient,
        email,
        login,
        password,
        status_code,
    ):
        url = f"{self.URL_PREFIX}"
        response = await ac.post(
            url,
            json={"email": email, "password": password, "login": login},
        )

        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )

    @pytest.mark.parametrize("email, password, status_code", USERS_LOGIN)
    async def test_login(self, ac: AsyncClient, email, password, status_code):
        login_url = "/auth/jwt/login"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "",
            "username": email,
            "password": password,
        }
        response = await ac.post(login_url, headers=headers, data=data)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )
