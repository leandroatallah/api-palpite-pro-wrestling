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


class SeasonSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True


class RequestSeason(BaseModel):
    parameter: SeasonSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: int = 200
    status: str
    message: str
    result: Optional[T]


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserOut(BaseModel):
    id: int
    email: str


class SystemUser(UserOut):
    password: str
