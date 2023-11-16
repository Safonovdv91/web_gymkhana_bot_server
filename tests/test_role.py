import pytest
from httpx import AsyncClient

# from src.roles.schemas import Role

"""
"""


class TestRole:
    url_prefix = "/api/v1/roles"

    ROLES_GOOD = [
        ("Admin_test", "Good description"),
        ("Admin_del_id", "Admin for deleting by id"),
        ("Admin_d_na", "Admin for deleting by name"),
        ("Admin_put", "Admin for put"),
        ("Admin_patch", "Admin for patch"),
        ("Admin_dup", "Admin2 original"),
    ]
    ROLES_BAD = [
        ("1@@Admin23", "G"),
        ("Admin", "qa"),
        ("1@@Admin23", 1),
        ("", ""),
    ]

    @pytest.mark.parametrize("role", ROLES_GOOD)
    async def test_add_role_ok(self, ac: AsyncClient, role, jwt_token):
        url = f"{self.url_prefix}/add"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.post(
            url,
            json={
                "name": role[0],
                "description": role[1],
            },
            cookies=cookies,
        )
        assert response.status_code == 201
        assert response.json()["data"]["name"] == role[0]
        assert response.json()["data"]["description"] == role[1]
        assert (
            response.json()["details"]
            == f"Adding role: [{role[0]} - {role[1]}] SUCCESS"
        )

    @pytest.mark.parametrize("role", ROLES_BAD)
    async def test_add_role_bad_credentials(
        self, ac: AsyncClient, role: tuple, jwt_token
    ):
        url = f"{self.url_prefix}/add"
        cookies = {"rabbitmg": jwt_token}

        response = await ac.post(
            url, json={"name": role[0], "description": role[1]}, cookies=cookies
        )
        assert response.status_code == 422, "bad credentials was add"

    async def test_add_role_duplicate(self, ac: AsyncClient, jwt_token):
        url = f"{self.url_prefix}/add"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.post(
            url,
            json={
                "name": "Admin_dup",
                "description": "Admin2 duplicate",
            },
            cookies=cookies,
        )
        assert response.status_code == 400, "Duplicate ROLE was added"
