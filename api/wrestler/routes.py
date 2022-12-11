from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import RequestWrestler, Response
import crud.wrestler as wrestler
from deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@router.post('/create')
async def create(request: RequestWrestler, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    wrestler.create_wrestler(db, request.parameter)
    return Response(code=200, status="OK", message="Wrestler created successfully").dict(exclude_none=True)


@router.get('/')
async def get(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _wrestler = wrestler.get_wrestler(db, 0, 100)
    return Response(code=200, status="Ok", message="Success fetch all data", result=_wrestler).dict(exclude_none=True)


@router.get('/{id}')
async def get_by_id(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _wrestler = wrestler.get_wrestler_by_id(db, id)
    return Response(code=200, status="Ok", message="Success get data", result=_wrestler).dict(exclude_none=True)


@router.post("/update")
async def update_wrestler(request: RequestWrestler, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(request.parameter)
    _wrestler = wrestler.update_wrestler(
        db, wrestler_id=request.parameter.id, name=request.parameter.name)
    return Response(code=200, status="Ok", message="Success update data", result=_wrestler).dict(exclude_none=True)


@router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    wrestler.remove_wrestler(db, wrestler_id=id)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)
