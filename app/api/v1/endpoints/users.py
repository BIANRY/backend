from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.crud_user import get_user, create_user, authenticate_user
from app.schemas.user import UserCreate, Token

router = APIRouter()

# 1) 회원가입
# POST /user/create
@router.post("/create")
def user_create(
    _user_create: UserCreate,
    db: Session = Depends(get_db),
):
    existing = get_user(db, student_id=_user_create.student_id)
    if existing:
        raise HTTPException(status_code=409, detail="이미 존재하는 학번입니다")

    create_user(db, _user_create)


# 2) 로그인
# POST /user/login
@router.post("/login", response_model=Token)
def user_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="학번 또는 비밀번호가 틀렸습니다",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.student_id},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")