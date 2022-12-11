from datetime import datetime
from sqlalchemy.orm import Session
from model import Wrestler
from schemas import WrestlerSchema


def get_wrestler(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Wrestler).offset(skip).limit(limit).all()


def get_wrestler_by_id(db: Session, wrestler_id: int):
    return db.query(Wrestler).filter(Wrestler.id == wrestler_id).first()


def create_wrestler(db: Session, wrestler: WrestlerSchema):
    _wrestler = Wrestler(name=wrestler.name)
    db.add(_wrestler)
    db.commit()
    db.refresh(_wrestler)
    return _wrestler


def remove_wrestler(db: Session, wrestler_id: int):
    _wrestler = get_wrestler_by_id(db=db, wrestler_id=wrestler_id)
    db.delete(_wrestler)
    db.commit()


def update_wrestler(db: Session, wrestler_id: int, name: str):
    _wrestler = get_wrestler_by_id(db=db, wrestler_id=wrestler_id)
    _wrestler.name = name
    db.commit()
    db.refresh(_wrestler)
    return _wrestler
