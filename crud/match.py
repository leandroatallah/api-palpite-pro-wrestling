from datetime import datetime
from sqlalchemy.orm import Session
from model import Match
from schemas import MatchSchema


def get_match(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Match).offset(skip).limit(limit).all()


def get_matches_by_event_id(db: Session, event_id: int):
    return db.query(Match).filter(Match.event_id == event_id).all()


def get_match_by_id(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()


def create_match(db: Session, match: MatchSchema):
    _match = Match(
        title=match.title,
        description=match.description,
        event_id=match.event_id,
        wrestler_one_id=match.wrestler_one_id,
        wrestler_two_id=match.wrestler_two_id
    )
    db.add(_match)
    db.commit()
    db.refresh(_match)
    return _match


def remove_match(db: Session, match_id: int):
    _match = get_match_by_id(db=db, match_id=match_id)
    db.delete(_match)
    db.commit()


def update_match(db: Session, match_id: int, title: str, description: str, event_id: int, wrestler_one_id: int, wrestler_two_id: int):
    _match = get_match_by_id(db=db, match_id=match_id)
    _match.title = title
    _match.description = description
    _match.event_id = event_id
    _match.wrestler_one_id = wrestler_one_id
    _match.wrestler_two_id = wrestler_two_id
    db.commit()
    db.refresh(_match)
    return _match
