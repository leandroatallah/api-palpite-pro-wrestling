from sqlalchemy.orm import Session
from model import Guess, Wrestler, Match
from schemas import GuessSchema


def get_guess(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Guess).offset(skip).limit(limit).all()


def get_guess_by_id(db: Session, guess_id: int):
    return db.query(Guess).filter(Guess.id == guess_id).first()


def get_guess_by_event_id(db: Session, event_id: int, user_id: int):
    guesses = db.query(Guess).filter(Guess.event_id ==
                                     event_id, Guess.user_id == user_id).all()
    result = []

    for guess in guesses:
        result.append({
            'id': guess.id,
            # 'event_id': guess.event_id,
            'winner_id': guess.winner_id,
            'match_id': guess.match_id,
            'result': guess.result,
            # 'match': guess.match
        })

    return result


def create_guess(db: Session, guess: GuessSchema, user_id: int):
    print(guess.match_id)
    _guess = Guess(user_id=user_id, match_id=guess.match_id, event_id=guess.event_id,
                   winner_id=guess.winner_id, result=guess.result)
    db.add(_guess)
    db.commit()
    db.refresh(_guess)
    return _guess


def update_guess(db: Session, guess_id: int, winner_id: int, result: str):
    _guess = get_guess_by_id(db=db, guess_id=guess_id)
    _guess.winner_id = winner_id
    _guess.result = result
    db.commit()
    db.refresh(_guess)
    return _guess
