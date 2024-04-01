from datetime import datetime
from typing import List, Optional, Annotated

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field, BeforeValidator

# from src.mongo_db import PyObjectId
from src.roles.schemas import RoleBase


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class SportClass(BaseModel):
    sport_class: Optional[str]
    description: Optional[str]


class UserModel(BaseModel):
    """
    Container for a single user record.
    """

    # The primary key for the UserModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    # Common information about user
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: Optional[EmailStr] = Field(alias="email", default=None)
    login: Optional[str] = Field(alias="username", default=None)
    first_name: Optional[str] = Field(alias="first_name", default=None)
    full_name: Optional[str] = Field(alias="full_name", default=None)
    country: Optional[str] = Field(alias="language_code", default=None)
    mention: Optional[str] = Field(alias="mention", default=None)
    # role: Optional[RoleBase] = Field(alias="role", default={"id": 1, "name": "Just user"})

    # Service information
    sub_stage: Optional[bool] = Field(alias="sub_stage", default=False)
    sub_ggp: Optional[bool] = Field(alias="sub_ggp", default=True)
    ggp_sub_classes: Optional[List | SportClass] = Field(alias="sub_stage_cat", default=[])
    registered_at: Optional[datetime] = Field(alias="register", default=datetime.now())
    # GGP PERCENTS block
    sub_ggp_percent: Optional[bool] = Field(
        alias="sub_ggp_percent", default=False
    )
    ggp_percent_begin: Optional[int] = Field(
        alias="ggp_percent_begin", default=100
    )
    ggp_percent_end: Optional[int] = Field(
        alias="ggp_percent_end", default=150
    )


class UsersCollection(BaseModel):
    """
    A container holding a list of `UserModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability]
    (https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    users: List[UserModel]


class UsersCollectionOut(BaseModel):
    status: Optional[str]
    data: Optional[List[UserModel]]
    details: Optional[str | int]
