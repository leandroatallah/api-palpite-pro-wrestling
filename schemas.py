import datetime
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class EventSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime.datetime] = None
    thumb: Optional[str] = None

    class Config:
        orm_mode = True


class RequestEvent(BaseModel):
    parameter: EventSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: int = 200
    status: str
    message: str
    result: Optional[T]
