from fastapi import APIRouter, Depends, Request
from starlette.templating import Jinja2Templates

from src.users.routers import get_users


router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/get_users")
def get_users_page(request: Request, usr=Depends(get_users)):
    return templates.TemplateResponse(
        "getusers.html", {"request": request, "users": usr["data"]}
    )


@router.get("/register")
def get_base_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
