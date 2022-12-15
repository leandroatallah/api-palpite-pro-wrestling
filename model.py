from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship, backref
from config import Base
import enum


@enum.unique
class MatchResult(enum.Enum):
    normal = 'normal'
    draw = 'draw'
    no_contest = 'no_contest'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    isSuperuser = Column(Boolean)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(DateTime)
    thumb = Column(String)
    status = Column(String)
    season_id = Column(Integer, ForeignKey("season.id"))
    matches = relationship('Match')


class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    event_id = Column(Integer, ForeignKey("event.id"))
    wrestler_one_id = Column(Integer, ForeignKey("wrestler.id"))
    wrestler_two_id = Column(Integer, ForeignKey("wrestler.id"))


class Wrestler(Base):
    __tablename__ = 'wrestler'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Season(Base):
    __tablename__ = 'season'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)


class Guess(Base):
    __tablename__ = 'guess'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    event_id = Column(Integer, ForeignKey("event.id"))
    match_id = Column(Integer, ForeignKey("match.id"))
    winner_id = Column(Integer, ForeignKey("wrestler.id"))
    # result = Column(Enum(MatchResult))
    result = Column(String)
    user = relationship(
        "User",
        backref=backref("user_guess", lazy="joined"),
        foreign_keys=[user_id],
        lazy="joined",
    )
    match = relationship(
        "Match",
        backref=backref("guesses", lazy="joined"),
        foreign_keys=[match_id],
        lazy="joined",
    )
