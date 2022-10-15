from fastapi import status, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from model import User
from schemas import UserSchema
from utils import create_access_token, create_refresh_token, get_hashed_password, verify_password


def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()


def create_user(db: Session, user: UserSchema):
    print(user)
    _user = get_user_by_email(db=db, user_email=user.email)
    if _user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    _user = User(email=user.email, password=get_hashed_password(user.password))
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def login_user(db: Session, user: UserSchema):
    _user = get_user_by_email(db=db, user_email=user.username)

    if _user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(hashed_pass, _user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }
