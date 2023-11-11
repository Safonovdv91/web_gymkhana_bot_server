import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.auth.auth_config import auth_backend, current_user, fastapi_users
from src.pages.routers import router as page_router
from src.pages.routers import templates
from src.users.models import User
from src.users.router_role import router_role
from src.users.router_user import router as auth_router
from src.users.schemas import UserCreate, UserRead


app = FastAPI(title="RabbitMG")

origins = [
    "http://localhost:5500",
    "https://localhost:5500",
    "http://127.0.0.1:5500",
    "https://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "not_exist.html", {"request": request}, status_code=404
        )
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
