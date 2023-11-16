import pytest
from httpx import AsyncClient


class TestApiUserPost:
    pass
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


class TestUserApiGetByEmail:
    common_url = "/api/v1/users"

    emails = [
        ("user3@example.com"),
        ("user1@example.com"),
        ("@@@"),
        ("123"),
    ]

    @pytest.mark.parametrize("email", emails)
    async def test_user_get_by_email(self, ac: AsyncClient, email):
        # url = f"{self.common_url}/get/email=user3@example.com"
        url = f"{self.common_url}/email={email}"
        response = await ac.get(url=url)
        if email == "user3@example.com":
            assert response.status_code == 200
            assert response.json()["data"]["email"] == "user3@example.com"
            assert response.json()["data"]["role"] == "User"
            assert response.json()["data"]["sub_ggp_percent"] is False, "Bad data"
            assert response.json()["data"]["ggp_percent_begin"] == 100, "Bad data"
            assert response.json()["data"]["ggp_percent_end"] == 150, "Bad data"
            assert response.json()["data"]["sub_offline"] is False, "Bad data"
            assert response.json()["data"]["sub_ggp"] is False, "Bad data"
            assert response.json()["data"]["sub_world_record"] is False, "Bad data"

        elif email in ("@@@", "123"):
            assert response.status_code == 422
        else:
            assert response.status_code == 404

    async def test_user_get_by_email_not_exist(self, ac: AsyncClient):
        url = f"{self.common_url}/email=usernotexist@example.com/get"
        response = await ac.get(url=url)
        assert response.status_code == 404, "Not exist user -> not 404"

    # async def test_user_get_verified(self, ac: AsyncClient, login_cookies):
    #     url = "/users/get"
    #     response = await ac.get(url=url, cookies=login_cookies)
    #     assert response.status_code == 200
    #     assert response.json()["data"]["email"] == "user3@example.com"

    @pytest.mark.asyncio
    async def test_get_current_user(self, jwt_token, ac: AsyncClient):
        # Пример тестирования другого эндпоинта, требующего аутентификации через cookies
        test_url = (
            "http://127.0.0.1:8000/api/v1/users/current"  # Замените на реальный URL
        )
        cookies = {"rabbitmg": jwt_token}
        response = await ac.get(test_url, cookies=cookies)

        assert response.status_code == 200
        assert response.json()["data"]["email"] == "for_login@example.com"
        # Добавьте дополнительные проверки для ответа, если необходимо


class TestUserApiDeleteByEmail:
    common_url = "/api/v1/users"
    emails = [
        ("user_for_delete@example.com"),
        ("usernoexist@example.com"),
        ("@@@"),
        ("123"),
        (),
    ]

    async def test_register_post(self, ac: AsyncClient):
        response = await ac.post(
            "/auth/register",
            json={
                "email": "user_for_delete@example.com",
                "password": "string",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "login": "string",
            },
        )
        assert response.status_code == 201, "User add register"

    @pytest.mark.parametrize("email", emails)
    async def test_user_delete_by_email(self, ac: AsyncClient, email):
        url = f"{self.common_url}/email={email}/delete"
        response = await ac.delete(url)

        if email == "user_for_delete@example.com":
            assert response.status_code == 200, "delete exist user not status 200"
            assert (
                response.json()["status"] == "Success"
            ), "delete exist user not status 200"
            assert (
                response.json()["details"] == "Was deleted!"
            ), "delete exist user not status 200"
        elif email == "usernoexist@example.com":
            assert response.status_code == 404
        else:
            assert response.status_code == 422

    async def test_check_user_delete_by_email_check(self, ac: AsyncClient):
        url = f"{self.common_url}/email=user_for_delete@example.com"
        response = await ac.get(url)
        assert response.status_code == 404

    async def test_get_current_user(self, ac: AsyncClient, jwt_token):
        # Пример тестирования другого эндпоинта, требующего аутентификации через cookies
        test_url = (
            "http://127.0.0.1:8000/api/v1/users/current"  # Замените на реальный URL
        )
        cookies = {"rabbitmg": jwt_token}
        response = await ac.get(test_url, cookies=cookies)

        assert response.status_code == 200
        assert response.json()["data"]["email"] == "for_login@example.com"
        # Добавьте дополнительные проверки для ответа, если необходимо
