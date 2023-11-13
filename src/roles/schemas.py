import re
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel
from pydantic.v1 import validator


class RoleRead(BaseModel):
    id: int
    name: str
    description: str


class CreatedResponse(BaseModel):
    status: int
    data: dict
    details: str


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
