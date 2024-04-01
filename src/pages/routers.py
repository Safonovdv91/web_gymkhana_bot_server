from fastapi import APIRouter, Depends, HTTPException, Request
from starlette.templating import Jinja2Templates

from src.config import BRANCH_NAME, PULL_REQUEST, SERVER_STATE, PATH_STATIC
from src.users.router import get_current_user, get_user_by_id, get_users, get_users_mongo

router = APIRouter(tags=["Frontend"])
templates = Jinja2Templates(directory="src/frontend/templates")
# templates = Jinja2Templates(directory=f"{PATH_STATIC}/templates")

@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse(
        name="base.html", context={"request": request}
    )


@router.get("/current_user")
def get_current_user_page(request: Request, users=Depends(get_current_user)):
    return templates.TemplateResponse(
        name="getusers.html",
        context={
            "PULL_REQUEST": PULL_REQUEST,
            "SERVER_STATE": SERVER_STATE,
            "BRANCH_NAME": BRANCH_NAME,
            "request": request,
            "users": [users["data"]],
        },
    )


@router.get("/get_users")
# def get_users_page(request: Request, users=Depends(get_users)):
def get_users_page(request: Request, users=Depends(get_users_mongo)):

    return templates.TemplateResponse(
        name="getusers.html",
        context={
            "PULL_REQUEST": PULL_REQUEST,
            "SERVER_STATE": SERVER_STATE,
            "BRANCH_NAME": BRANCH_NAME,
            "request": request,
            "users": users["data"],
        },
    )


@router.get("/grid")
def get_users_page_grid(request: Request, users=Depends(get_users)):
    return templates.TemplateResponse(
        name="grid.html",
        context={
            "PULL_REQUEST": PULL_REQUEST,
            "SERVER_STATE": SERVER_STATE,
            "BRANCH_NAME": BRANCH_NAME,
            "request": request,
            "users": users["data"],
        },
    )


@router.get("/get_users/{user_id}")
def get_users_page_id(request: Request, usr=Depends(get_user_by_id)):
    try:
        user_data = usr["data"]
        return templates.TemplateResponse(
            name="getusers.html",
            context={
                "PULL_REQUEST": PULL_REQUEST,
                "BRANCH_NAME": BRANCH_NAME,
                "SERVER_STATE": SERVER_STATE,
                "request": request,
                "users": [user_data],
            },
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/registration")
def get_register_page(request: Request):
    return templates.TemplateResponse(
        name="registration.html",
        context={"SERVER_STATE": SERVER_STATE, "request": request},
    )


@router.get("/login")
async def get_login_page(
    request: Request,
):
    return templates.TemplateResponse("login.html", {"request": request})
