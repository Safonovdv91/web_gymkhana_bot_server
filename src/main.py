import uvicorn
from fastapi import Depends, FastAPI
from starlette.staticfiles import StaticFiles

from src.auth.auth_config import auth_backend, current_user, fastapi_users
from src.pages.routers import router as page_router
from src.users.models import User
from src.users.routers import router as auth_router
from src.users.routers import router_role
from src.users.schemas import UserCreate, UserRead


app = FastAPI(title="RabbitMG")

app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth", "user"],
)

app.include_router(auth_router)
app.include_router(router_role)
app.include_router(page_router)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.login} you are {user.email} and your role is {user.role_id}"


# # Создание главного роутера
# main_api_router = APIRouter()
# # настройка роутеров для
# main_api_router.include_router(
#     user_router, prefix="/user", tags=["user2", "login"]
# )
# app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
