from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import RequestGuess, Response
import crud.guess as guess
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
    guess.create_guess(db, request.parameter)
    return Response(code=200, status="OK", message="Guess created successfully").dict(exclude_none=True)


@router.get('/')
async def get(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _guess = guess.get_guess(db, 0, 100)

    return Response(code=200, status="Ok", message="Success fetch all data", result=_guess).dict(exclude_none=True)


@router.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _guess = guess.get_guess_by_id(db, id)
    return Response(code=200, status="Ok", message="Success get data", result=_guess).dict(exclude_none=True)


@router.post("/update")
async def update_guess(request: RequestGuess, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(request.parameter)
    _guess = guess.update_guess(db, user=request.parameter.user, match=request.parameter.match,
                                winner=request.parameter.winner,)
    return Response(code=200, status="Ok", message="Success update data", result=_guess).dict(exclude_none=True)


@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    guess.remove_guess(db, guess_id=id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)
