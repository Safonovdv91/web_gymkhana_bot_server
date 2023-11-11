import re
from datetime import datetime
from typing import Annotated

from annotated_types import MaxLen, MinLen
from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import BaseModel, EmailStr
from pydantic.v1 import validator


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


class RoleCreate(BaseModel):
    name: Annotated[
        str,
        MinLen(3),
        MaxLen(25),
    ]
    description: Annotated[str, MinLen(3)]

    @validator("name")
    def name_regex(cls, v):
        if not re.match(r"^[a-zA-Z]+$", v):
            raise ValueError(
                "Only letters, numbers, and underscore are allowed in the name"
            )
        return v


class RoleRead(BaseModel):
    id: int
    name: str
    description: str


class CreatedResponse(BaseModel):
    status: int
    data: dict
    details: str
