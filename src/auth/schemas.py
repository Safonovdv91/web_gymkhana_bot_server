import re
from datetime import datetime

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    ggp_percent_begin: int
    ggp_percent_end: int
    sub_ggp_percent: bool
    sub_offline: bool
    sub_ggp: bool
    sub_world_record: bool
    telegram_id: str | None
    registered_at: datetime
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    login: str
    email: EmailStr
    password: str


class RoleCreate(BaseModel):
    name: str
    description: str


class RoleRead(BaseModel):
    id: str
    name: str
    description: str


class OkResponse(BaseModel):
    status: int
    data: dict
    details: str


class CreatedResponse(BaseModel):
    status: int
    data: dict
    details: str
