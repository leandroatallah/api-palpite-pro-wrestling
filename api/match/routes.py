from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import RequestMatch, Response
import crud.match as match
from deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@router.post('/create')
async def create(request: RequestMatch, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    match.create_match(db, request.parameter)
    return Response(code=200, status="OK", message="Match created successfully").dict(exclude_none=True)


@router.get('/')
async def get(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _match = match.get_match(db, 0, 100)
    return Response(code=200, status="Ok", message="Success fetch all data", result=_match).dict(exclude_none=True)


@router.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _match = match.get_match_by_id(db, id)
    return Response(code=200, status="Ok", message="Success get data", result=_match).dict(exclude_none=True)


@router.post("/update")
async def update_match(request: RequestMatch, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(request.parameter)
    _match = match.update_match(
        db,
        match_id=request.parameter.id,
        title=request.parameter.title,
        description=request.parameter.description,
        status=request.parameter.status,
        # event_id=request.parameter.event_id,
        # guesses=request.parameter.guesses,
        wrestlers=request.parameter.wrestlers
    )
    return Response(code=200, status="Ok", message="Success update data", result=_match).dict(exclude_none=True)


@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    match.remove_match(db, match_id=id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)
