import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi_users import FastAPIUsers

from src.auth.auth import auth_backend
from src.auth.manager import get_user_manager
from src.auth.models import UserDAL, User
from src.auth.schemas import UserCreate, UserRead
from src.database import async_session_maker


app = FastAPI(title="RabbitMG")

user_router = APIRouter()


# ----------
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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
# -------



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
            )


@user_router.post("/")
async def create_user(body: UserCreate):
    result = await _create_new_user(body)
    return {"status": "success", "data": result, "details": None}


# Создание главного роутера
main_api_router = APIRouter()
# настройка роутеров для
main_api_router.include_router(
    user_router, prefix="/user", tags=["user", "login"]
)
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
