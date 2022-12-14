from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import RequestEvent, Response
import crud.event as event
from deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@router.post('/create')
async def create(request: RequestEvent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event.create_event(db, request.parameter)
    return Response(code=200, status="OK", message="Event created successfully").dict(exclude_none=True)


@router.get('/')
async def get(db: Session = Depends(get_db), user: User = Depends(get_current_user), season_id: int | None = None, event_status: str | None = None):
    if season_id:
        _event = event.get_events_by_season_id(
            db, season_id=season_id, user=user)
    elif event_status:
        _event = event.get_events_by_status(db, status=event_status, user=user)
    else:
        _event = event.get_event(db, 0, 100, user=user)
    return Response(code=200, status="Ok", message="Success fetch all data", result=_event).dict(exclude_none=True)


@router.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _event = event.get_event_by_id(db, id)
    return Response(code=200, status="Ok", message="Success get data", result=_event).dict(exclude_none=True)


@router.post("/update")
async def update_event(request: RequestEvent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _event = event.update_event(db, event_id=request.parameter.id, status=request.parameter.status,
                                title=request.parameter.title, description=request.parameter.description,
                                date=request.parameter.date, thumb=request.parameter.thumb,
                                season_id=request.parameter.season_id)
    return Response(code=200, status="Ok", message="Success update data", result=_event).dict(exclude_none=True)


@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event.remove_event(db, event_id=id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)
