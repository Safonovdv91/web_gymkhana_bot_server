import re
from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen
from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import BaseModel, EmailStr

from ..roles.schemas import RoleBase
from ..sport_classes.schemas import SportClassResponseOne


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserRead(schemas.BaseUser):
    # id: int
    # email: EmailStr
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
    password: Annotated[str, MinLen(4)]


class UserOut(BaseModel):
    id: int = 1
    email: EmailStr = "user1@mail.com"
    ggp_percent_begin: int = 100
    ggp_percent_end: int = 150
    sub_ggp_percent: bool = True
    sub_offline: bool = False
    sub_ggp: bool = True
    sub_world_record: bool = False
    telegram_id: str | None = "239123941"
    registered_at: datetime
    role: RoleBase
    ggp_sub_classes: list[SportClassResponseOne]
    # role_id: int


class UserResponseMany(BaseModel):
    status: str = "Success"
    data: list[UserOut]
    details: str | dict | None = {"count": 10}


class UserResponseOne(BaseModel):
    status: str = "Success"
    data: UserOut
    details: str | None = None


class SUser(BaseModel):
    email: EmailStr = "user1@mail.com"
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class SResponse(BaseModel):
    status: str
    details: str | dict | None = None


class SUserOutput(SUser):
    telegram_id: str | None = "239123941"
    registered_at: datetime
    role: RoleBase


class SUserOutResponseOne(SResponse):
    data: SUserOutput


class SUserOutResponseMany(SResponse):
    data: list[SUserOutput]


class SUserSearchArgs:
    def __init__(
        self,
        is_active: Optional[bool] = None,
        role: Optional[str] = None,
        sub_offline: Optional[bool] = None,
    ):
        self.is_active = is_active
        self.role = role
        self.sub_offline = sub_offline
