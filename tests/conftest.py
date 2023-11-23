import asyncio
import json
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.database import get_async_session
from src.database import metadata
from src.config import (
    DB_HOST_TEST,
    DB_NAME_TEST,
    DB_PASS_TEST,
    DB_PORT_TEST,
    DB_USER_TEST,
)
from src.main import app
from src.roles.models import Role
from src.users.models import User

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    def open_mock_json(model: str):
        with open(f"mock_{model}.json", "r") as file:
            return json.load(file)

    roles = open_mock_json(model="roles")
    users = open_mock_json(model="users")
    async with async_session_maker() as session:
        add_roles = insert(Role).values(roles)
        add_users = insert(User).values(users)
        await session.execute(add_roles)
        await session.execute(add_users)
        await session.commit()


# From pytest-asyncio documentation
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def jwt_token(ac: AsyncClient):
    """
    Фикстура получения jwt куки для авторизации пользователя
    """
    login_url = "/auth/jwt/login"
    test_username = "for_login@example.com"
    test_password = "string"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": f"{test_username}",
        "password": f"{test_password}",
    }
    response = await ac.post(login_url, headers=headers, data=data)
    assert (
        response.status_code == 204
    ), f"fixture: Problem with login user: [{test_username}]"
    return response.cookies["rabbitmg"]


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
