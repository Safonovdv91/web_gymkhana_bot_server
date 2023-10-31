import uvicorn
from fastapi import APIRouter, FastAPI
from src.auth.models import UserDAL
from src.auth.schemas import ShowUser, UserCreate
from src.database import async_session_maker


app = FastAPI(title="RabbitMG")

user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session_maker() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                login=body.login, password=body.password, email=body.email
            )
            return ShowUser(
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
