import json

import pytest
from httpx import AsyncClient

# from src.roles.schemas import Role

"""
"""


class TestRole:
    URL_PREFIX = "/api/v1/roles"


class TestRoleAdd(TestRole):
    ROLES = [
        ("Admin_test", "Good description", 201),
        ("Admin_del_id", "Admin for deleting by id", 201),
        ("Admin_del_name", "Admin for deleting by name", 201),
        ("Admin_put", "Admin for put", 201),
        ("Admin_patch", "Admin for patch", 201),
        ("Admin_dup", "Admin2 original", 201),
        ("Admin_dup", "Admin2 original", 400),
        ("Admin_duasdasdsdsadasdasdp", "Admin2 original", 422),
        ("", "Admin2 original", 422),
    ]

    @pytest.mark.parametrize("role_name, role_description, status_code", ROLES)
    async def test_add_role(
        self, ac: AsyncClient, role_name, role_description, status_code, jwt_token
    ):
        url = f"{self.URL_PREFIX}/add"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.post(
            url,
            json={
                "name": role_name,
                "description": role_description,
            },
            cookies=cookies,
        )
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )


class TestRoleGet(TestRole):
    COUNT_OF_ROLE = 10
    ROLES = [
        (1, "mock_owner", 200),
        ("2", "mock_admin", 200),
        (3, "mock_user", 200),
        (1000, "iisi", 404),
        # ("", "Admin", 422),
        ("sda", "User", 422),
        (3, "mock_user", 200),
    ]

    ROLES_NAME = [
        ("mock_owner", "mock_owner_discriotion", 200),
        ("mock_owner2", "mock_owner_discriotion", 404),
    ]

    BAD_ROLES_EMAIL = [
        (123, "Test of admin"),
        ("", "Test of user"),
        ("@#!", "Test of guest"),
    ]

    async def test_get_roles(self, ac: AsyncClient, jwt_token):
        url = f"{self.URL_PREFIX}"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == 200
        assert (
            len(response.json()["data"]) == self.COUNT_OF_ROLE
        ), f"Count of role incorrect {len(response.json()['data'])}"

    async def test_get_roles_unauthorized(self, ac: AsyncClient):
        url = f"{self.URL_PREFIX}"
        response = await ac.get(url=url)
        assert response.status_code == 401

    @pytest.mark.parametrize("role_id, expected_role_name, status_code", ROLES)
    async def test_get_role_by_id(
        self,
        ac: AsyncClient,
        jwt_token,
        role_id: int,
        expected_role_name: str,
        status_code,
    ):
        url = f"{self.URL_PREFIX}/id={role_id}"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )
        if response.status_code == 200:
            assert response.json()["data"]["name"] == expected_role_name

    @pytest.mark.parametrize("role_id, expected_role_name, status", ROLES)
    async def test_get_role_by_id_unauthirized(
        self, ac: AsyncClient, role_id: int, expected_role_name: str, status
    ):
        url = f"{self.URL_PREFIX}/id={role_id}"
        response = await ac.get(url=url)
        assert response.status_code == 401, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )

    @pytest.mark.parametrize("name, role_desc, status", ROLES_NAME)
    async def test_get_role_by_name(
        self, ac: AsyncClient, name: str, role_desc: str, status, jwt_token
    ):
        url = f"{self.URL_PREFIX}/name={name}"

        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == status
        if status == 200:
            assert response.json()["data"]["description"] == role_desc

    @pytest.mark.parametrize("role_email", BAD_ROLES_EMAIL)
    async def test_get_role_by_email_not_exist(
        self, ac: AsyncClient, jwt_token, role_email
    ):
        url = f"{self.URL_PREFIX}/name={role_email}"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == 404

    @pytest.mark.parametrize("role_email, role_description, status", ROLES_NAME)
    async def test_get_role_by_email_unauthorized(
        self, ac: AsyncClient, role_email: str, role_description: str, status
    ):
        url = f"{self.URL_PREFIX}/name={role_email}"
        response = await ac.get(url=url)
        assert response.status_code == 401


class TestRoleDelete(TestRole):
    ROLE_FOR_DELETE_ID = "Admin_del_id"
    ROLE_FOR_DELETE_NAME = "Admin_del_name"

    async def test_delete_role_by_id_ok(self, ac: AsyncClient, jwt_token):
        url_get = f"{self.URL_PREFIX}/name={self.ROLE_FOR_DELETE_ID}"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(url=url_get, cookies=cookies)

        id_role_delete = response.json()["data"]["id"]
        url_del = f"{self.URL_PREFIX}/id={id_role_delete}/delete"
        assert response.status_code == 200, "Role doesn't exist"
        response = await ac.delete(url=url_del, cookies=cookies)

        assert response.status_code == 200, "Deleting bad"

        response = await ac.get(url=url_get, cookies=cookies)
        assert response.status_code == 404, "Deleting not work, user exist"

    async def test_delete_role_by_name_unauthorized(self, ac: AsyncClient):
        url_del = f"{self.URL_PREFIX}/name={self.ROLE_FOR_DELETE_NAME}/delete"
        response = await ac.delete(url=url_del)

        assert response.status_code == 401, "Unauthorized not work"

    async def test_delete_role_by_name_ok(self, ac: AsyncClient, jwt_token):
        url_get = f"{self.URL_PREFIX}/name={self.ROLE_FOR_DELETE_NAME}"
        url_del = f"{url_get}/delete"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(url=url_get, cookies=cookies)
        assert response.status_code == 200, "Role doesn't exist"
        response = await ac.delete(url=url_del, cookies=cookies)

        assert response.status_code == 200, "Deleting bad"
        response = await ac.get(url=url_get, cookies=cookies)
        assert response.status_code == 404, "Deleting not work, user exist"

    async def test_delete_role_by_id_unauthorized(self, ac: AsyncClient):
        url_del = f"{self.URL_PREFIX}/id={self.ROLE_FOR_DELETE_ID}/delete"
        response = await ac.delete(url=url_del)

        assert response.status_code == 401, "Unauthorized not work"


class TestRoleUpdate(TestRole):
    ROLE_FOR_PUT_NAME = "Admin_put"
    ROLE_FOR_PATCH_NAME = "Admin_patch"

    async def test_role_put(self, ac: AsyncClient, jwt_token):
        url_get = f"{self.URL_PREFIX}/name={self.ROLE_FOR_PUT_NAME}"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(
            url=url_get,
            cookies=cookies,
        )

        id_role = response.json()["data"]["id"]

        url_put = f"{self.URL_PREFIX}/id={id_role}/update"
        assert response.status_code == 200, "Role doesn't exist"
        assert response.json()["data"]["name"] == "Admin_put"
        response = await ac.put(
            url=url_put,
            cookies=cookies,
            json={
                "name": "Admin_up",
                "description": "UPGRADED",
            },
        )

        assert response.status_code == 200, "Put bad"
        response = await ac.get(url=f"{self.URL_PREFIX}/id={id_role}", cookies=cookies)
        assert response.status_code == 200, "Updateing not work, user exist"
        assert response.json()["data"]["name"] == "Admin_up", "PUT name not work"
        assert (
            response.json()["data"]["description"] == "UPGRADED"
        ), "Put discription not work"

    async def test_role_put_unauthorized(self, ac: AsyncClient, jwt_token):
        url_get = f"{self.URL_PREFIX}/name={self.ROLE_FOR_PATCH_NAME}"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(
            url=url_get,
            cookies=cookies,
        )

        id_role = response.json()["data"]["id"]

        url_put = f"{self.URL_PREFIX}/id={id_role}/update"
        assert response.status_code == 200, "Role doesn't exist"
        assert response.json()["data"]["name"] == "Admin_patch"
        response = await ac.put(
            url=url_put,
            json={
                "name": "Admin_up",
                "description": "UPGRADED",
            },
        )
        assert response.status_code == 401, "Unauthorized problem"

        response = await ac.get(url=f"{self.URL_PREFIX}/id={id_role}", cookies=cookies)
        assert response.status_code == 200, "Updateing not work, user exist"
        assert response.json()["data"]["name"] == "Admin_patch", "PUT name not work"
        assert (
            response.json()["data"]["description"] == "Admin for patch"
        ), "Put discription not work"

    async def test_role_patch(self, ac: AsyncClient, jwt_token):
        url_get = f"{self.URL_PREFIX}/name={self.ROLE_FOR_PATCH_NAME}"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(
            url=url_get,
            cookies=cookies,
        )

        id_role = response.json()["data"]["id"]

        url_put = f"{self.URL_PREFIX}/id={id_role}/update"
        assert response.status_code == 200, "Role doesn't exist"
        assert response.json()["data"]["name"] == "Admin_patch"
        response = await ac.patch(
            url=url_put,
            cookies=cookies,
            json={
                "description": "UPGRADED",
            },
        )
        assert response.status_code == 200, "PATCH BAD"
        response = await ac.get(url=f"{self.URL_PREFIX}/id={id_role}", cookies=cookies)
        assert response.status_code == 200, "Updateing not work, user exist"
        assert response.json()["data"]["name"] == "Admin_patch", "PUT name not work"
        assert (
            response.json()["data"]["description"] == "UPGRADED"
        ), "Put discription not work"
