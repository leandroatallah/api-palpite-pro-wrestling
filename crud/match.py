from datetime import datetime
from sqlalchemy.orm import Session
from model import Match
from schemas import MatchSchema


def get_match(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Match).offset(skip).limit(limit).all()


def get_match_by_id(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()


def create_match(db: Session, match: MatchSchema):
    _match = Match(
        title=match.title,
        description=match.description,
        event_id=match.event_id,
        guesses=match.guesses,
        wrestlers=match.wrestlers,
    )
    db.add(_match)
    db.commit()
    db.refresh(_match)
    return _match


def remove_match(db: Session, match_id: int):
    _match = get_match_by_id(db=db, match_id=match_id)
    db.delete(_match)
    db.commit()


def update_match(db: Session, match_id: int, title: str, description: str, event_id: int, guesses: tuple, wrestlers: tuple):
    _match = get_match_by_id(db=db, match_id=match_id)
    _match.title = title
    _match.description = description
    _match.event_id = event_id
    _match.guesses = guesses
    _match.wrestlers = wrestlers
    db.commit()
    db.refresh(_match)
    return _match
