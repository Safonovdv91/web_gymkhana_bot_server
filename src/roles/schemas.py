import re
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict
from pydantic.v1 import validator


class RoleBase(BaseModel):
    name: str
    description: str


class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RoleResponseOne(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    status: str
    data: Role
    details: str | None


class RoleResponseMany(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    status: str
    data: list[Role]
    details: str | None


class CreatedResponse(BaseModel):
    status: int
    data: RoleBase
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
