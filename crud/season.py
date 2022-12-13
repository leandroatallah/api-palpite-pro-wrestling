from sqlalchemy.orm import Session
from model import Season
from schemas import SeasonSchema


def get_season(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Season).offset(skip).limit(limit).all()


def get_season_by_id(db: Session, season_id: int):
    return db.query(Season).filter(Season.id == season_id).first()


def create_season(db: Session, season: SeasonSchema):
    _season = Season(title=season.title, status=season.status)
    db.add(_season)
    db.commit()
    db.refresh(_season)
    return _season


def remove_season(db: Session, season_id: int):
    _season = get_season_by_id(db=db, season_id=season_id)
    db.delete(_season)
    db.commit()


def update_season(db: Session, season_id: int, title: str, status: str):
    _season = get_season_by_id(db=db, season_id=season_id)
    _season.title = title
    _season.status = status
    db.commit()
    db.refresh(_season)
    return _season
