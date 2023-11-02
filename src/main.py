import uvicorn
from fastapi import Depends, FastAPI

from src.auth.auth_config import auth_backend, fastapi_users
from src.auth.models import User, UserDAL
from src.auth.schemas import UserCreate, UserRead
from src.database import async_session_maker


app = FastAPI(title="RabbitMG")

current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.login} you are {user.email} and your role is {user.role_id}"


fake_user = [{"user1": 1}, {"user2": 2}]


@app.get("/users")
async def get_user():
    result = [*fake_user]
    return {"status": "success", "data": result, "details": None}


@app.get("/roles/{role_id}")
async def get_role(role_id):
    return {"status": "success", "data": role_id, "details": None}


async def _create_new_user(body: UserCreate) -> UserRead:
    async with async_session_maker() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                login=body.login, password=body.password, email=body.email
            )
            return UserRead(
                id=user.id,
                ggp_percent_begin=user.ggp_percent_begin,
                ggp_percent_end=user.ggp_percent_end,
                sub_ggp_percent=user.sub_ggp_percent,
                sub_offline=user.sub_offline,
                sub_ggp=user.sub_ggp,
                sub_world_record=user.sub_world_record,
                telegram_id=user.telegram_id,
                login=user.login,
                email=user.email,
                registered_at=user.registered_at,
                is_active=user.is_active,
            )


# # Создание главного роутера
# main_api_router = APIRouter()
# # настройка роутеров для
# main_api_router.include_router(
#     user_router, prefix="/user", tags=["user2", "login"]
# )
# app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
