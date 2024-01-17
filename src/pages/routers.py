from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.templating import Jinja2Templates

from src.users.router import get_user_by_id, get_users


router = APIRouter(tags=["Frontend"])
templates = Jinja2Templates(directory="src/frontend/templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/get_users")
def get_users_page(
        request: Request,
        users=Depends(get_users)
):
    return templates.TemplateResponse(
        name="getusers.html",
        context={"request": request, "users": users["data"]}
    )


@router.get("/get_users/{user_id}")
def get_users_page_id(request: Request, usr=Depends(get_user_by_id)):
    try:
        user_data = usr["data"]
        return templates.TemplateResponse(
            "getusers.html", {"request": request, "users": [user_data]}
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/registration")
def get_register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/login")
async def get_login_page(
    request: Request,
):
    return templates.TemplateResponse("authorization.html", {"request": request})
