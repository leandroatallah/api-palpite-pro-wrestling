from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import RequestGuess, Response
import crud.guess as guess
from crud.user import get_user_by_email
from deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@router.post('/create')
async def create(request: RequestGuess, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _user = get_user_by_email(db=db, user_email=user.sub)
    guess.create_guess(db=db, guess=request.parameter, user_id=_user.id)
    return Response(code=200, status="OK", message="Guess created successfully").dict(exclude_none=True)


@router.get('/{event_id}')
async def get_by_id(event_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _user = get_user_by_email(db=db, user_email=user.sub)
    _guess = guess.get_guess_by_event_id(
        db=db, event_id=event_id, user_id=_user.id)
    return Response(code=200, status="Ok", message="Success get data", result=_guess).dict(exclude_none=True)


@ router.post("/update")
async def update_guess(request: RequestGuess, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _user = get_user_by_email(db=db, user_email=user.sub)
    _guess = guess.update_guess(
        db, guess_id=request.parameter.id, winner_id=request.parameter.winner_id, result=request.parameter.result)
    return Response(code=200, status="Ok", message="Success update data", result=_guess).dict(exclude_none=True)
