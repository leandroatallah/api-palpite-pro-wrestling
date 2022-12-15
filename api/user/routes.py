from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import Response, RequestUser
import crud.user as user
from crud.user import get_user_by_email
from deps import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@router.get('/')
async def get(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = user.get_users(db, 0, 100)
    return Response(code=200, status="Ok", message="Success fetch all data", result=result).dict(exclude_none=True)


@router.post('/signup')
async def create_user(request: RequestUser, db: Session = Depends(get_db)):
    user.create_user(db, request.parameter)
    return Response(code=200, status="OK", message="User created successfully").dict(exclude_none=True)


@router.patch('/edit-password')
async def edit_user_password(request: RequestUser, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user.edit_user_password(
        db=db, user_email=current_user.parameter.sub, password=request.parameter.password)
    return Response(code=200, status="OK", message="User password updated successfully").dict(exclude_none=True)


@router.patch('/promote/{id}')
async def promote_user(id: int, request: RequestUser, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user.promote_user(db=db, id=id, user_email=current_user.sub)
    return Response(code=200, status="OK", message="User promoted successfully").dict(exclude_none=True)


@ router.delete('/{id}')
async def delete(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user.remove_user(db, id, user_email=current_user.sub)
    return Response(code=200, status="Ok", message="Success delete data").dict(exclude_none=True)


@ router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user.login_user(db, form_data)


@ router.get('/me')
async def get_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _user = get_user_by_email(db, current_user.sub)
    result = {
        'email': _user.email,
        'isSuperuser': _user.isSuperuser,
        'guess_count': _user.guess_count,
    }
    return Response(code=200, status="Ok", message="Success fetch all data", result=result).dict(exclude_none=True)
