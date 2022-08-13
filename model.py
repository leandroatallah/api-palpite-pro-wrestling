from sqlalchemy import Column, Integer, String, DateTime
from config import Base


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(DateTime)
    thumb = Column(String)
