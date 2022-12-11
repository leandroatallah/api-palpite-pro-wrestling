from datetime import datetime
from sqlalchemy.orm import Session
from model import Event
from schemas import EventSchema


def get_event(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).offset(skip).limit(limit).all()


def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def create_event(db: Session, event: EventSchema):
    _event = Event(title=event.title, description=event.description,
                   date=event.date, thumb=event.thumb)
    db.add(_event)
    db.commit()
    db.refresh(_event)
    return _event


def remove_event(db: Session, event_id: int):
    _event = get_event_by_id(db=db, event_id=event_id)
    db.delete(_event)
    db.commit()


def update_event(db: Session, event_id: int, title: str, description: str,
                 date: datetime, thumb: str):
    _event = get_event_by_id(db=db, event_id=event_id)
    _event.title = title
    _event.description = description
    _event.date = date
    _event.thumb = thumb
    db.commit()
    db.refresh(_event)
    return _event
