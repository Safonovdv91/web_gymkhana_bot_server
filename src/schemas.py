from pydantic import BaseModel


class OkResponse(BaseModel):
    status: int
    data: dict
    details: str
