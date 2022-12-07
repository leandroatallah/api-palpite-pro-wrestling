from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from config import SessionLocal
from sqlalchemy.orm import Session
from model import User
from schemas import Response, UserSchema
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


@router.post('/signup')
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    user.create_user(db, request)
    return Response(code=200, status="OK", message="User created successfully").dict(exclude_none=True)


@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return user.login_user(db, form_data)


@router.get('/me')
async def get_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _user = get_user_by_email(db, current_user.sub)
    result = {
        'email': _user.email,
        'isSuperuser': _user.isSuperuser,
    }
    return Response(code=200, status="Ok", message="Success fetch all data", result=result).dict(exclude_none=True)
