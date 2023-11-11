import pytest
from httpx import AsyncClient


class TestApiUserPost:
    pass


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
