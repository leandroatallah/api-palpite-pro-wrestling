from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from urllib import request
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestUser, Response
import crud.user as user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@router.post('/signup')
async def create_user(request: RequestUser, db: Session = Depends(get_db)):
    user.create_user(db, request.parameter)
    return Response(code=200, status="OK", message="User created successfully").dict(exclude_none=True)


@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user.login_user(db, form_data)

# @router.get('/')
# async def get(email: str, db: Session = Depends(get_db)):
#     _user = user.get_user_by_email(db, email)
#     return Response(code=200, status="Ok", message="Success fetch all data", result=_user).dict(exclude_none=True)
