import pytest
from httpx import AsyncClient

# from src.roles.schemas import Role

"""
"""


class TestRole:
    URL_PREFIX = "/api/v1/roles"


class TestRoleAdd(TestRole):
    ROLES_GOOD = [
        ("Admin_test", "Good description"),
        ("Admin_del_id", "Admin for deleting by id"),
        ("Admin_del_name", "Admin for deleting by name"),
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
        url = f"{self.URL_PREFIX}/add"
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
        url = f"{self.URL_PREFIX}/add"
        cookies = {"rabbitmg": jwt_token}

        response = await ac.post(
            url, json={"name": role[0], "description": role[1]}, cookies=cookies
        )
        assert response.status_code == 422, "bad credentials was add"

    async def test_add_role_duplicate(self, ac: AsyncClient, jwt_token):
        url = f"{self.URL_PREFIX}/add"
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


class TestRoleGet(TestRole):
    COUNT_OF_ROLE = 9
    ROLES_ID = [
        (1, "Admin"),
        ("2", "User"),
        (3, "Guest"),
    ]

    BAD_ROLES_ID = [
        ("", "Admin"),
        ("sda", "User"),
        (3, "Guest"),
    ]

    ROLES_EMAIL = [
        ("Admin", "Test of admin"),
        ("User", "Test of user"),
        ("Guest", "Test of guest"),
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
        ), "Count of role incorrect"

    async def test_get_roles_unauthorized(self, ac: AsyncClient):
        url = f"{self.URL_PREFIX}"
        response = await ac.get(url=url)
        assert response.status_code == 401

    @pytest.mark.parametrize("role_id, expected_role_name", ROLES_ID)
    async def test_get_role_by_id(
        self, ac: AsyncClient, jwt_token, role_id: int, expected_role_name: str
    ):
        url = f"{self.URL_PREFIX}/id={role_id}"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == 200
        assert response.json()["data"]["name"] == expected_role_name

    @pytest.mark.parametrize("role_id", BAD_ROLES_ID)
    async def test_get_role_by_id_bad_id(self, ac: AsyncClient, jwt_token, role_id):
        url = f"{self.URL_PREFIX}/id={role_id}"
        cookies = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == 422

    @pytest.mark.parametrize("role_id, expected_role_name", ROLES_ID)
    async def test_get_role_by_id_unauthirized(
        self, ac: AsyncClient, role_id: int, expected_role_name: str
    ):
        url = f"{self.URL_PREFIX}/id={role_id}"
        response = await ac.get(url=url)
        assert response.status_code == 401

    @pytest.mark.parametrize("role_email, role_description", ROLES_EMAIL)
    async def test_get_role_by_email(
        self, ac: AsyncClient, jwt_token, role_email: str, role_description: str
    ):
        url = f"{self.URL_PREFIX}/name={role_email}"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == 200
        assert response.json()["data"]["description"] == role_description

    @pytest.mark.parametrize("role_email", BAD_ROLES_EMAIL)
    async def test_get_role_by_email_not_exist(
        self, ac: AsyncClient, jwt_token, role_email
    ):
        url = f"{self.URL_PREFIX}/name={role_email}"
        cookies: dict = {"rabbitmg": jwt_token}
        response = await ac.get(url=url, cookies=cookies)
        assert response.status_code == 404

    @pytest.mark.parametrize("role_email, role_description", ROLES_EMAIL)
    async def test_get_role_by_email_unauthorized(
        self, ac: AsyncClient, role_email: str, role_description: str
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
