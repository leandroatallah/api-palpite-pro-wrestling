from datetime import datetime
from sqlalchemy.orm import Session
from model import Event
from schemas import EventSchema


def get_event(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).offset(skip).limit(limit).all()


def get_events_by_season_id(db: Session, season_id: int):
    return db.query(Event).filter(Event.season_id == season_id).all()


def get_events_by_status(db: Session, status: str):
    return db.query(Event).filter(Event.status == status).all()


def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()


def create_event(db: Session, event: EventSchema):
    _event = Event(status=event.status, title=event.title, description=event.description,
                   date=event.date, thumb=event.thumb, season_id=event.season_id)
    db.add(_event)
    db.commit()
    db.refresh(_event)
    return _event


def remove_event(db: Session, event_id: int):
    _event = get_event_by_id(db=db, event_id=event_id)
    db.delete(_event)
    db.commit()


def update_event(db: Session, event_id: int, status: str, title: str, description: str,
                 date: datetime, thumb: str, season_id: int):
    _event = get_event_by_id(db=db, event_id=event_id)
    _event.status = status
    _event.title = title
    _event.description = description
    _event.date = date
    _event.thumb = thumb
    _event.season_id = season_id
    db.commit()
    db.refresh(_event)
    return _event
