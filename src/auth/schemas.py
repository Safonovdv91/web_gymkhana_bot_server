import re
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TuneModel(BaseModel):
    """
    Модель конвертирующая любой объект в json
    """

    class Config:
        orm_mode = True


class ShowUser(TuneModel):
    id: int
    ggp_percent_begin: int
    ggp_percent_end: int
    sub_ggp_percent: bool
    sub_offline: bool
    sub_ggp: bool
    sub_world_record: bool
    telegram_id: str | None
    registered_at: datetime


class UserCreate(BaseModel):
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
