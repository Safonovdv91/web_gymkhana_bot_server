import re
from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen, MinLen
from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
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


class BaseUserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str


class UserCreate(BaseUserCreate):
    login: Annotated[str, MinLen(3), MaxLen(14)]
    email: EmailStr
    password: Annotated[str, MinLen(4)]


class UserResponseMany(BaseModel):
    status: str
    data: list[UserRead]
    details: str | dict | None


class UserResponseOne(BaseModel):
    status: str
    data: list[UserRead]
    details: str | None
