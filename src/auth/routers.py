from src.auth.auth_config import auth_backend, fastapi_users
from src.main import app
from src.users.schemas import UserCreate, UserRead


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
