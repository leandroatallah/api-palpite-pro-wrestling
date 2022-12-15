import datetime
from typing import Optional, Generic, TypeVar, List, Union
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from sqlalchemy.orm import relationship
# from model import MatchResult

T = TypeVar('T')


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True


class WrestlerSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        orm_mode = True


class SeasonSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True


class GuessSchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    event_id: Optional[int] = None
    match_id: Optional[int] = None
    winner_id: Optional[int] = None
    # result: MatchResult = None
    result: Optional[str] = None

    class Config:
        orm_mode = True


class MatchSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    event_id: Optional[int] = None
    wrestler_one_id: Optional[int] = None
    wrestler_two_id: Optional[int] = None
    guesses: "List[GuessSchema]" = None

    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime.datetime] = None
    thumb: Optional[str] = None
    status: Optional[str] = None
    matches: List[MatchSchema] = None
    season_id: Optional[int] = None

    class Config:
        orm_mode = True


class RequestSeason(BaseModel):
    parameter: SeasonSchema = Field(...)


class RequestEvent(BaseModel):
    parameter: EventSchema = Field(...)


class RequestMatch(BaseModel):
    parameter: MatchSchema = Field(...)


class RequestWrestler(BaseModel):
    parameter: WrestlerSchema = Field(...)


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)


class RequestGuess(BaseModel):
    parameter: GuessSchema = Field(...)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class Response(GenericModel, Generic[T]):
    code: int = 200
    status: str
    message: str
    result: Optional[T]


class UserOut(BaseModel):
    id: int
    email: str


class SystemUser(UserOut):
    password: str
