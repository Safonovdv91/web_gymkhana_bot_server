import json

import pytest
from httpx import AsyncClient


class TestUserApiGetByEmail:
    common_url = "/api/v1/users"
    USERS = [
        ("user3@example.com", 200),
        ("not_exissdt@test.com", 404),
        ("@@@", 422),
        ("123", 422),
        ("", 422),
    ]

    @pytest.mark.parametrize("email, status_code", USERS)
    async def test_user_get_by_email(
        self, ac: AsyncClient, email, status_code, jwt_token
    ):
        url = f"{self.common_url}/?email={email}"
        response = await ac.get(url=url, cookies=jwt_token)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )

    @pytest.mark.parametrize("email, status", USERS)
    async def test_user_get_by_email_unauthorized(self, ac: AsyncClient, email, status):
        url = f"{self.common_url}/?email={email}"
        response = await ac.get(url=url)
        assert response.status_code == 401, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )

    @pytest.mark.asyncio
    async def test_get_current_user(self, jwt_token, ac: AsyncClient):
        # Пример тестирования другого эндпоинта, требующего аутентификации через cookies
        test_url = "http://127.0.0.1:8000/api/v1/users/current"  #
        response = await ac.get(test_url, cookies=jwt_token)

        assert response.status_code == 200
        assert response.json()["data"]["email"] == "for_login@example.com"
        # Добавьте дополнительные проверки для ответа, если необходимо


class TestUserApiDeleteByEmail:
    common_url = "/api/v1/users"
    USERS_FOR_DELETE = [
        ("for_delete@example.com", 200),
        ("user1sdaa@example.com", 404),
        ("@@@", 422),
        ("123", 422),
    ]

    @pytest.mark.parametrize("email, status_code", USERS_FOR_DELETE)
    async def test_user_delete_by_email(
        self, ac: AsyncClient, email, status_code, jwt_token
    ):
        url = f"{self.common_url}/?email={email}"
        if status_code == 200:
            response = await ac.get(url, cookies=jwt_token)
            assert response.status_code == 200, f"User {email} not exist"

        url = f"{self.common_url}/email={email}/delete"
        response = await ac.delete(url=url, cookies=jwt_token)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )

        if status_code == 200:
            url = f"{self.common_url}/?email={email}"
            response = await ac.get(url, cookies=jwt_token)
            assert response.status_code == 404, f"User {email} is not delete"

    @pytest.mark.parametrize("email, status_code", USERS_FOR_DELETE)
    async def test_user_delete_by_email_unauthorized(
        self, ac: AsyncClient, email, status_code
    ):
        url = f"{self.common_url}/email={email}/delete"

        response = await ac.delete(url=url)
        assert response.status_code == 401, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )
