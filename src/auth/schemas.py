import re
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from fastapi_users import schemas


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TuneModel(BaseModel):
    """
    Модель конвертирующая любой объект в json
    """

    class Config:
        orm_mode = True


class UserShow(TuneModel):
    id: int
    ggp_percent_begin: int
    ggp_percent_end: int
    sub_ggp_percent: bool
    sub_offline: bool
    sub_ggp: bool
    sub_world_record: bool
    telegram_id: str | None
    registered_at: datetime

class UserRead(schemas.BaseUser[int]):

    id: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False



class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

class UserCreate2(BaseModel):
    login: str
    password: str
    email: EmailStr

    @field_validator("login")
    def validate_login(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Login should contains only latters"
            )
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str

