import json

import pytest
from httpx import AsyncClient
from faker import Faker


class FakeUser:
    def __init__(self, user_id: int):
        fake = Faker()
        self.user_id = user_id
        self.email = fake.email()
        self.ggp_percent_begin = fake.random_int(50, 130)
        self.ggp_percent_end = fake.random_int(self.ggp_percent_begin, 200)
        self.sub_ggp_percent = fake.boolean()
        self.sub_offline = fake.boolean()
        self.sub_ggp = fake.boolean()
        self.sub_world_record = fake.boolean()
        self.telegram_id = str(fake.random_int(1_000_000, 1_000_000_000))

    def __repr__(self):
        return f"{self.user_id}, {self.email}, {self.ggp_percent_begin}, {self.ggp_percent_end}," \
               f" {self.sub_ggp_percent}, {self.sub_offline}, {self.sub_ggp}, {self.sub_world_record}, {self.telegram_id}"

    def __str__(self):
        return self.__repr__()


users = (FakeUser(i) for i in range(5, 6))


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
        url = f"{self.common_url}/"
        params = {"email": email}
        response = await ac.get(url=url, cookies=jwt_token, params=params)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )

    @pytest.mark.parametrize("email, status", USERS)
    async def test_user_get_by_email_unauthorized(self, ac: AsyncClient, email, status):
        url = f"{self.common_url}/"
        params = {"email": email}
        response = await ac.get(url=url, params=params)
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
        url = f"{self.common_url}/"
        params = {"email": email}
        if status_code == 200:
            response = await ac.get(url, cookies=jwt_token, params=params)
            assert response.status_code == 200, f"User {email} not exist"

        url = f"{self.common_url}/email={email}/delete"
        response = await ac.delete(url=url, cookies=jwt_token)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )

        if status_code == 200:
            url = f"{self.common_url}/"
            response = await ac.get(url, cookies=jwt_token, params=params)
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


class TestUserApiGetById:
    COMMON_URL = "/api/v1/users"
    USERS = [
        (1, 200, "user3@example.com"),
        (2, 200, "user1@example.com"),
        (101010, 404, None),
        ("101010", 404, None),
        ("@@@", 422, None),
        ("12k", 422, None),
        ("", 404, None),
    ]

    @pytest.mark.parametrize("user_id, status_code, email", USERS)
    async def test_user_get_by_id(
            self, ac: AsyncClient, user_id, status_code, email, jwt_token
    ):
        url = f"{self.COMMON_URL}/id={user_id}"
        response = await ac.get(url=url, cookies=jwt_token)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )
        if status_code == 200:
            assert response.json()["data"]["email"] == email, (
                f"STATUS: [{response.status_code}]\n "
                f"{json.dumps(response.json(), indent=4)}"
            )

    @pytest.mark.parametrize("user_id, status, email", USERS)
    async def test_user_get_by_id_unauthorized(
            self, ac: AsyncClient, user_id, status, email
    ):
        url = f"{self.COMMON_URL}/id={user_id}"
        response = await ac.get(url=url)
        assert response.status_code in (401, 404), (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )


class TestUsersApiGetByRoles:
    COMMON_URL = "/api/v1/users/"

    USERS = [
        (1, 200, 0, "user3@example.com"),
        ("1", 200, 1, "user1@example.com"),
        ("bb", 422, 0, None),
        ("", 404, 0, None),
    ]

    @pytest.mark.parametrize("role_id, status_code, count_user, email", USERS)
    async def test_user_get_by_id(
            self, ac: AsyncClient, role_id, status_code, count_user, email, jwt_token: dict
    ):
        url = f"{self.COMMON_URL}role={role_id}"
        response = await ac.get(url=url, cookies=jwt_token)
        assert response.status_code == status_code, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )
        if status_code == 200:
            assert response.json()["data"][count_user]["email"] == email, (
                f"STATUS: [{response.status_code}]\n "
                f"{json.dumps(response.json(), indent=4)}"
            )

    @pytest.mark.parametrize("role_id, status, count_user,email", USERS)
    async def test_user_get_by_role_id_unauthorized(
            self, ac: AsyncClient, role_id, status, count_user, email
    ):
        url = self.COMMON_URL
        response = await ac.get(url=url)
        assert response.status_code == 401, (
            f"STATUS: [{response.status_code}]\n "
            f"{json.dumps(response.json(), indent=4)}"
        )


# class TestUserPatchUserSubscribeById:
#     """
#     Проверяем метод подписки/отписки пользователя от спортивных классов в GGP
#     посылается id пользователя и буква класса или список букв(из существубщих классов)
#     """
#
#     USER_SUB = [
#         (1, "A", 200, "user3@example.com", 1),
#         (1, "B", 200, "user3@example.com", 2),
#         (1, "B", 200, "user3@example.com", 1),
#         (1, "C1", 200, "user3@example.com", 2),
#         (1, "C2", 200, "user3@example.com", 3),
#         (1, "C3", 200, "user3@example.com", 4),
#         (1, "D1", 200, "user3@example.com", 5),
#         (1, "D2", 200, "user3@example.com", 6),
#         (1, "D2", 200, "user3@example.com", 5),
#         (1, "D1", 200, "user3@example.com", 4),
#         (1, "C3", 200, "user3@example.com", 3),
#         (1, "C2", 200, "user3@example.com", 2),
#         (1, "C1", 200, "user3@example.com", 1),
#         (1, "A", 200, "user3@example.com", 0),
#         (2, "B", 200, "user1@example.com", 1),
#         (2, "C5", 422, "user1@example.com", 1),
#         (2, "1", 422, "user1@example.com", 1),
#         (2, "-1", 422, "user1@example.com", 1),
#         (2, "", 422, "user1@example.com", 1),
#         (2, "B", 200, "user1@example.com", 0),
#         (150, "B", 404, None, 0),
#     ]
#     URL = "/api/v1/users/"
#
#     @pytest.mark.parametrize(
#         "user_id, sub_letter, status_code, email, length_subscribe", USER_SUB
#     )
#     async def test_user_subscribe_class(
#             self,
#             ac: AsyncClient,
#             user_id,
#             sub_letter,
#             status_code,
#             email,
#             length_subscribe,
#             jwt_token: dict,
#     ):
#         url_subscribe = f"{self.URL}id={user_id}/subscribe"
#         data = {"sport_class": sub_letter}
#         response = await ac.patch(
#             url=url_subscribe, cookies=jwt_token, content=json.dumps(data)
#         )
#         assert response.status_code == status_code, (
#             f"STATUS: [{response.status_code}]\n "
#             f"{json.dumps(response.json(), indent=4)}"
#         )
#         if status_code == 200:
#             assert response.json()["data"]["email"] == email, (
#                 f"STATUS: [{response.status_code}]\n "
#                 f"{json.dumps(response.json(), indent=4)}"
#             )
#
#         # Проверка валидности через метод получения инфы через get by id
#         url_subscribe = f"{self.URL}id={user_id}"
#         response = await ac.get(url=url_subscribe, cookies=jwt_token)
#         if response.status_code not in [404]:
#             assert response.status_code == 200, (
#                 f"STATUS: [{response.status_code}]\n "
#                 f"{json.dumps(response.json(), indent=4)}"
#             )
#             assert response.json()["data"]["email"] == email, (
#                 f"STATUS: [{response.status_code}]\n "
#                 f"{json.dumps(response.json(), indent=4)}"
#             )
#             assert (
#                     len(response.json()["data"]["ggp_sub_classes"]) == length_subscribe
#             ), (
#                 f"STATUS: [{response.status_code}]\n "
#                 f"{json.dumps(response.json(), indent=4)}"
#             )
#
#     @pytest.mark.parametrize(
#         "user_id, sub_letter, status_code, email, length_subscribe", USER_SUB
#     )
#     async def test_user_sub_class_unauthorized(
#             self,
#             ac: AsyncClient,
#             user_id,
#             sub_letter,
#             status_code,
#             email,
#             length_subscribe,
#             jwt_token: dict,
#     ):
#         url_subscribe = f"{self.URL}id={user_id}/subscribe"
#         data = {"sport_class": sub_letter}
#         response = await ac.patch(url=url_subscribe, content=json.dumps(data))
#         assert response.status_code == 401, (
#             f"STATUS: [{response.status_code}]\n "
#             f"{json.dumps(response.json(), indent=4)}"
#         )
#
#         # Проверка валидности через метод получения инфы через get by id
#         if status_code not in [404]:
#             url_subscribe = f"{self.URL}id={user_id}"
#             response = await ac.get(url=url_subscribe, cookies=jwt_token)
#             assert response.status_code == 200, (
#                 f"STATUS: [{response.status_code}]\n "
#                 f"{json.dumps(response.json(), indent=4)}"
#             )
#             assert response.json()["data"]["email"] == email, (
#                 f"STATUS: [{response.status_code}]\n "
#                 f"{json.dumps(response.json(), indent=4)}"
#             )
#             assert len(response.json()["data"]["ggp_sub_classes"]) == 0, (
#                 f"STATUS: [{response.status_code}]\n "
#                 f"{json.dumps(response.json(), indent=4)}"
#             )


class TestUserPatchUserById:
    """
    Тестирование /api/v1/users/id={user_id}/patch
    изменения данных о пользователе
    """
    URL = "/api/v1/users"
    USER_PATCH = [(user, 200) for user in users]

    @pytest.mark.parametrize(
        "user, status_code", USER_PATCH
    )
    async def test_user_patch_by_id(
            self,
            ac: AsyncClient,
            user: FakeUser,
            status_code,
            jwt_token
    ):
        """
        Позитивный тест на апгрейд всех данных польхователя
        """
        url_patch = f"{self.URL}/id=5/patch"
        url_get = f"{self.URL}/id=5"
        data = {
            "user_id": user.user_id,
            "email": user.email,
            "ggp_percent_begin": user.ggp_percent_begin,
            "ggp_percent_end": user.ggp_percent_end,
            "sub_ggp_percent": user.sub_ggp_percent,
            "sub_offline": user.sub_offline,
            "sub_ggp": user.sub_ggp,
            "sub_world_record": user.sub_world_record,
            "telegram_id": user.telegram_id
        }
        response = await ac.get(url=url_get, cookies=jwt_token)
        assert response.status_code == 200, "user not exist"

        response = await ac.patch(
            url=url_patch, cookies=jwt_token, content=json.dumps(data)
        )
        assert response.status_code == 200, "user not patched"

        response = await ac.get(url=url_get, cookies=jwt_token)
        assert response.status_code == 200, "user not exist"
        assert response.json()["data"]["email"] == user.email, "Email not patched"
        assert response.json()["data"]["ggp_percent_begin"] == user.ggp_percent_begin, f"begin % not valid"
        assert response.json()["data"]["ggp_percent_end"] == user.ggp_percent_end, f"end % not valid"
        assert response.json()["data"]["sub_ggp_percent"] == user.sub_ggp_percent, f"sub % not valid"
        assert response.json()["data"]["sub_offline"] == user.sub_offline, f"sub OFFLINE not valid"
        assert response.json()["data"]["sub_ggp"] == user.sub_ggp, f"sub GGP not valid"
        assert response.json()["data"]["sub_world_record"] == user.sub_world_record, f"sub WORLD  not valid"

    @pytest.mark.parametrize(
        "user, status_code", USER_PATCH
    )
    async def test_user_patch_by_id_particular(
            self,
            ac: AsyncClient,
            user: FakeUser,
            status_code,
            jwt_token
    ):
        """
        Позитивный тест на апгрейд частичных данных польхователя
        """
        url_patch = f"{self.URL}/id=5/patch"
        url_get = f"{self.URL}/id=5"

        response = await ac.get(url=url_get, cookies=jwt_token)
        assert response.status_code == 200, "Не удалось получить данные пользователя"

        old_data = response.json()["data"]
        print(old_data)

        data = {
            "user_id": user.user_id,
            "email": user.email,
            "ggp_percent_begin": user.ggp_percent_begin,
            "ggp_percent_end": user.ggp_percent_end,
            "sub_ggp_percent": user.sub_ggp_percent,
            "sub_offline": user.sub_offline,
            "sub_ggp": user.sub_ggp,
            "sub_world_record": user.sub_world_record,
            "telegram_id": user.telegram_id
        }
        print(f"keys: {data.keys()}")
        for k, v in data.items():
            response = await ac.patch(url=url_patch, cookies=jwt_token, content=json.dumps({k: v}))
            print(json.dumps({k: v}))
            assert response.status_code == 200, (
                f"STATUS: [{response.status_code}]\n "
                f"Content = {json.dumps({k: v})}\n"
                f"{json.dumps(response.json(), indent=4)}"
            )
            response = await ac.get(url=f"{self.URL}/id=5", cookies=jwt_token)
            print(response.json()["data"])
            print()
