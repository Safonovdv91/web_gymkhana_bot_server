from pydantic import BaseModel


class SportClassSchema(BaseModel):
    sport_class: str
    description: str


class SportClassResponse(BaseModel):
    id: int
    sport_class: str
    description: str


class SportClassResponseMany(BaseModel):
    status: str
    data: list[SportClassSchema]
    details: str | dict | None
