from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from config import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    isSuperuser = Column(Boolean)


class Match(Base):
    __tablename__ = 'match'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    event_id = Column(Integer, ForeignKey("event.id"))


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(DateTime)
    thumb = Column(String)
    matches = relationship('Match')
