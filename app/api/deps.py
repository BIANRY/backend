from typing import Generator

import jwt
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import oauth2_scheme
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import TokenData


def get_db() -> Generator:
    """
    Dependency(의존성) 함수.
    API 요청 하나당 DB 세션을 열고, 요청이 끝나면 반드시 닫습니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    from app.crud.crud_user import get_user  # 순환 참조 방지
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
