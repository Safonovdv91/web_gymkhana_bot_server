import pytest
from httpx import AsyncClient


class TestApiUser:

    async def test_register_post(self, ac: AsyncClient):
        response = await ac.post("/auth/register", json={
            "email": "user_for_delete@example.com",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "login": "string"
        })
        assert response.status_code == 201, "User add register"

    # async def test_user_get_unauthorized(ac: AsyncClient):
    #     response = await ac.get("/api/v1/users/get", )
    #     assert response.status_code == 401, "UnAuthorized "

    # @pytest.fixture
    # async def login_cookies(ac: AsyncClient):
    #     url = "/auth/jwt/login"
    #     data = {
    #         "username": "user3@example.com",
    #         "password": "string",
    #     }
    #     response = await ac.post(url=url, data=data)
    #     return response.cookies


class TestUserApi:
    common_url = "/api/v1/users"

    emails = [
        ("user3@example.com"),
        ("user1@example.com"),
        ("@@@"),
        ("123"),
    ]

    @pytest.mark.parametrize('email', emails)
    async def test_user_get_by_id_ok(self, ac: AsyncClient, email):
        # url = f"{self.common_url}/get/email=user3@example.com"
        url = f"{self.common_url}/get/email={email}"
        response = await ac.get(url=url)
        if email == "user3@example.com":
            assert response.status_code == 200
            assert response.json()["data"]["email"] == "user3@example.com"
        elif email in ("@@@", "123"):
            assert response.status_code == 422
        else:
            assert response.status_code == 404

    async def test_user_get_by_id_(self, ac: AsyncClient):
        url = f"{self.common_url}/get/email=usernotexist@example.com"
        response = await ac.get(url=url)
        assert response.status_code == 404, "Not exist user -> not 404"

    # async def test_user_get_verified(self, ac: AsyncClient, login_cookies):
    #     url = "/users/get"
    #     response = await ac.get(url=url, cookies=login_cookies)
    #     assert response.status_code == 200
    #     assert response.json()["data"]["email"] == "user3@example.com"
