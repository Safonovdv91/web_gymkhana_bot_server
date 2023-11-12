import pytest
from httpx import AsyncClient


@pytest.fixture
async def jwt_token(ac: AsyncClient):
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
    print(response.cookies["rabbitmg"])
    return response.cookies["rabbitmg"]


@pytest.mark.asyncio
async def test_authenticated_endpoint(jwt_token, ac: AsyncClient):
    # Пример тестирования другого эндпоинта, требующего аутентификации через cookies
    test_url = "http://127.0.0.1:8000/api/v1/users/current"  # Замените на реальный URL
    cookies = {"rabbitmg": jwt_token}
    response = await ac.get(test_url, cookies=cookies)

    assert response.status_code == 200
    print(response.json())
    # Добавьте дополнительные проверки для ответа, если необходимо


class TestRole:
    url_prefix = "/api/v1/roles"

    roles = [
        ("Admin", "Good description"),
        ("Admin2", "Good description"),
        ("1@@Admin23", "G"),
        ("Admin2", "Good description"),
        ("Admin", "qa"),
        ("1@@Admin23",),
        ("", ""),
        (),
    ]

    @pytest.mark.parametrize("adding_role", roles)
    async def test_add_role(self, ac: AsyncClient, adding_role):
        url = f"{self.url_prefix}/add"
        response = await ac.post(
            url,
            json={
                "name": adding_role,
                "description": "Good description",
            },
        )
        if adding_role == "Admin":
            assert response.status_code == 200
            assert response.json()["data"]["role"] == adding_role[0]
            assert response.json()["data"]["description"] == adding_role[1]
            assert response.json()["details"] == f"Adding role: {adding_role} success"
        else:
            assert response.status_code == 422

    async def test_add_role_duplicate(self, ac: AsyncClient):
        url = f"{self.url_prefix}/add"
        response = await ac.post(
            url,
            json={
                "name": "Admin2",
                "description": "Good description",
            },
        )
        assert response.status_code == 400
