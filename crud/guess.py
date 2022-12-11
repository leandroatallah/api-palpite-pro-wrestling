from sqlalchemy.orm import Session
from model import Guess
from schemas import GuessSchema


def get_guess(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Guess).offset(skip).limit(limit).all()


def get_guess_by_id(db: Session, guess_id: int):
    return db.query(Guess).filter(Guess.id == guess_id).first()


def create_guess(db: Session, guess: GuessSchema):
    _guess = Guess(user=guess.user, match=guess.match, winner=guess.winner)

    db.add(_guess)
    db.commit()
    db.refresh(_guess)
    return _guess


def remove_guess(db: Session, guess_id: int):
    _guess = get_guess_by_id(db=db, guess_id=guess_id)
    db.delete(_guess)
    db.commit()


def update_guess(db: Session, guess_id: int, winner: int):
    _guess = get_guess_by_id(db=db, guess_id=guess_id)
    _guess.winner = winner
    db.commit()
    db.refresh(_guess)
    return _guess
