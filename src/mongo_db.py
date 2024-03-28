
from typing import Optional, List

import uvicorn
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument

from src.config import DB_HOST_MONGO, DB_PORT_MONGO

app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
client = motor.motor_asyncio.AsyncIOMotorClient(f"{DB_HOST_MONGO}:{DB_PORT_MONGO}")
db = client.users_bot
student_collection = db.get_collection("users")

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    """
    Container for a single student record.
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

    # Service information
    sub_stage: Optional[bool] = Field(alias="sub_stage", default=False)
    sub_ggp: Optional[bool] = Field(alias="sub_ggp", default=True)
    ggp_sub_classes: Optional[List] = Field(alias="sub_stage_cat", default=[])
    ggp_percent_begin: int = 100
    ggp_percent_end: int = 150
    sub_ggp_percent: bool = True
    #
    # model_config = ConfigDict(
    #     populate_by_name=True,
    #     arbitrary_types_allowed=True,
    # )


class UpdateUserModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    course: Optional[str] = None
    gpa: Optional[float] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )


class UserCollection(BaseModel):
    """
    A container holding a list of `UserModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    students: List[UserModel]


@app.post(
    "/students/",
    response_description="Add new student",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_student(student: UserModel = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    new_student = await student_collection.insert_one(
        student.model_dump(by_alias=True, exclude=["id"])
    )
    created_student = await student_collection.find_one(
        {"_id": new_student.inserted_id}
    )
    return created_student


@app.get(
    "/users/",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_students():
    """
    List all of the student data in the database.
    The response is unpaginated and limited to 1000 results.
    """
    print(await student_collection.find().to_list(1000))
    users = await student_collection.find().to_list(1000)
    # return {
    #     "status": "Success",
    #     "data": users,
    #     "details": {"count_users": len(users)},
    # }
    return UserCollection(students=await student_collection.find().to_list(1000))


@app.get(
    "/users/{id}",
    response_description="Get a single student",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def show_student(id: str):
    """
    Get the record for a specific student, looked up by `id`.
    """
    if (
        student := await student_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put(
    "/students/{id}",
    response_description="Update a student",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def update_student(id: str, student: UpdateUserModel = Body(...)):
    """
    Update individual fields of an existing student record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    student = {
        k: v for k, v in student.model_dump(by_alias=True).items() if v is not None
    }

    if len(student) >= 1:
        update_result = await student_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": student},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_student := await student_collection.find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/students/{id}", response_description="Delete a student")
async def delete_student(id: str):
    """
    Remove a single student record from the database.
    """
    delete_result = await student_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
