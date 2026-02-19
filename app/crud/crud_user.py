from typing import Annotated

import jwt
from fastapi import HTTPException, status
from fastapi.params import Depends
from jose import JWTError
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, oauth2_scheme
from app.models.user import User
from app.schemas.user import UserCreate, TokenData


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)

    db_user = User(
        name=user.name,
        student_id=user.student_id,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, student_id: str):
    return db.query(User).filter(User.student_id == student_id).first()


def authenticate_user(db: Session, student_id: str, password: str):
    user = get_user(db, student_id=student_id)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(db: Session, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        student_id: str = payload.get("sub")
        if student_id is None:
            raise credentials_exception
        token_data = TokenData(student_id=student_id)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db=db, student_id=token_data.student_id)
    if user is None:
        raise credentials_exception
    return user
