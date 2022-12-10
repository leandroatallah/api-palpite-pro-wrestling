from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import RequestSeason, Response
import crud.season as season
from deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@router.post('/create')
async def create(request: RequestSeason, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    season.create_season(db, request.parameter)
    return Response(code=200, status="OK", message="Season created successfully").dict(exclude_none=True)


@router.get('/')
async def get(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _season = season.get_season(db, 0, 100)
    return Response(code=200, status="Ok", message="Success fetch all data", result=_season).dict(exclude_none=True)


@router.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _season = season.get_season_by_id(db, id)
    return Response(code=200, status="Ok", message="Success get data", result=_season).dict(exclude_none=True)


@router.post("/update")
async def update_season(request: RequestSeason, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(request.parameter)
    _season = season.update_season(db, season_id=request.parameter.id, title=request.parameter.title,
                                   status=request.parameter.status)
    return Response(code=200, status="Ok", message="Success update data", result=_season).dict(exclude_none=True)


@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    season.remove_season(db, season_id=id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)
