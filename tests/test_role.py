import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_user(jwt_token, ac: AsyncClient):
    # Пример тестирования другого эндпоинта, требующего аутентификации через cookies
    test_url = "http://127.0.0.1:8000/api/v1/users/current"  # Замените на реальный URL
    cookies = {"rabbitmg": jwt_token}
    response = await ac.get(test_url, cookies=cookies)

    assert response.status_code == 200
    assert response.json()["data"]["email"] == "for_login@example.com"
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
    async def test_add_role(self, ac: AsyncClient, adding_role, jwt_token):
        url = f"{self.url_prefix}/add"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.post(
            url,
            json={
                "name": adding_role,
                "description": "Good description",
            },
            cookies=cookies,
        )
        if adding_role == "Admin":
            assert response.status_code == 200
            assert response.json()["data"]["role"] == adding_role[0]
            assert response.json()["data"]["description"] == adding_role[1]
            assert response.json()["details"] == f"Adding role: {adding_role} success"
        else:
            assert response.status_code == 422

    async def test_add_role_duplicate(self, ac: AsyncClient, jwt_token):
        url = f"{self.url_prefix}/add"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.post(
            url,
            json={
                "name": "Admin2",
                "description": "Good description",
            },
            cookies=cookies,
        )
        assert response.status_code == 400
