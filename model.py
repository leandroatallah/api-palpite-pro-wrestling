from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from config import Base

match_association = Table(
    'match_association',
    Base.metadata,
    Column('matches', ForeignKey('match.id')),
    Column('wrestlers', ForeignKey('wrestler.id')),
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    isSuperuser = Column(Boolean)
    guesses = relationship('Guess')


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
    guesses = relationship('Guess')
    wrestlers = relationship("Wrestler", secondary=match_association)


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
    user = Column(Integer, ForeignKey("user.id"))
    match = Column(Integer, ForeignKey("match.id"))
    winner = Column(Integer)
