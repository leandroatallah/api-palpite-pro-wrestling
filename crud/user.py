from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from model import User, Guess
from schemas import UserSchema
from utils import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login",
    scheme_name="JWT"
)

credentials_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).with_entities(User.id, User.email, User.isSuperuser).all()


def get_user_by_email(db: Session, user_email: str):
    _user = db.query(User).filter(User.email == user_email).first()
    guess_count = db.query(Guess).filter(
        Guess.user_id == _user.id).count()
    _user.guess_count = guess_count
    return _user


def create_user(db: Session, user: UserSchema):
    _user = get_user_by_email(db=db, user_email=user.email)
    if _user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    _user = User(email=user.email, password=get_hashed_password(
        user.password), isSuperuser=False)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def edit_user_password(db: Session, user_email: str, password: str):
    _user = get_user_by_email(db=db, user_email=user_email)
    _user.password = get_hashed_password(password)
    db.commit()
    db.refresh(_user)
    return _user


def promote_user(db: Session, id: int, user_email: str):
    current_user = get_user_by_email(db=db, user_email=user_email)
    _user = db.query(User).filter(User.id == id).first()

    if _user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't alter this user"
        )
    _user.isSuperuser = not _user.isSuperuser
    db.commit()
    db.refresh(_user)
    return _user


def remove_user(db: Session, id: int, user_email: str):
    current_user = get_user_by_email(db=db, user_email=user_email)
    _user = db.query(User).filter(User.id == id).first()

    if _user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't delete this user"
        )
    db.delete(_user)
    db.commit()


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
