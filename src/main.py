import time

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from logger.logger import init_logger
from src.admin_panel.views import RoleAdmin, SportClassAdmin, UserAdmin
from src.auth.auth_config import auth_backend, fastapi_users
from src.config import SITE_PORT, SITE_URL
from src.database import engine
from src.pages.routers import router as page_router, templates
from src.roles.router import router_role
from src.sport_classes.router import router as router_sport_class
from src.users.router import router as auth_router
from src.users.schemas import UserCreate, UserRead


logger = init_logger("main")
app = FastAPI(title="RabbitMG")

app.mount("/static", StaticFiles(directory="src/frontend/static"), "static")

origins = [
    f"http://localhost.{SITE_URL}:{SITE_PORT}",
    f"https://localhost.{SITE_URL}:{SITE_PORT}",
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    logger.info(
        request.headers,
        extra={"tags": {"middleware": "True", "content_type": "request"}},
    )
    try:
        response = await call_next(request)
    except Exception:
        logger.error(
            msg="all_proc error",
            extra={"tags": {"middleware": "True"}},
            exc_info=True,
        )
        raise HTTPException(status_code=404, detail="problem 404 in request")
    process_time = time.time() - start_time
    logger.info(
        f"time:{process_time}: \n{response.headers}",
        extra={"tags": {"middleware": "True", "content_type": "response"}},
    )
    response.headers["X-Process-Time"] = str(round(process_time, 5))
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 401:
        return templates.TemplateResponse(
            "login.html", {"request": request}, status_code=401
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
app.include_router(router_sport_class)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(SportClassAdmin)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
