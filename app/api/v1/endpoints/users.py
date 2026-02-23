from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.crud_user import get_user, create_user, authenticate_user
from app.models.user import User
from app.schemas.user import UserCreate, Token, UserUpdate, UserResponse, MyProfileResponse, PasswordResetRequest, PasswordResetVerify, PasswordResetConfirm


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


# 3) 내 정보 조회 (마이페이지)
# GET /users/me
@router.get("/me", response_model=MyProfileResponse)
def read_user_profile(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    from app.crud.crud_user import get_my_profile
    return get_my_profile(db, current_user)


# 4) 내 정보 수정
# PUT /users/me
@router.put("/me", response_model=UserResponse)
def update_user_profile(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    from app.crud.crud_user import update_user
    updated_user = update_user(db, current_user, user_update)
    return updated_user


# 5) 비밀번호 초기화 (요청)
# POST /users/password-reset/request
@router.post("/password-reset/request")
def request_password_reset(
    req: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    from app.crud.crud_user import get_user_by_email
    from app.crud.crud_verification import create_verification_code
    from app.core.email import send_verification_email
    import random
    from datetime import datetime, timedelta, timezone

    # 1. 일치하는 사용자가 있는지 확인
    user = get_user_by_email(db, email=req.email)
    if not user:
        # 보안 상 가입되지 않은 이메일이어도 동일하게 성공 메시지를 반환합니다.
        return {"msg": "이메일이 전송되었습니다. (가입된 이메일인 경우)"}

    # 2. 6자리 인증 코드 생성
    code = f"{random.randint(0, 999999):06d}"
    
    # 3. 만료 시간 설정 (예: 5분 후)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    
    # 4. DB에 인증 코드 저장 (이전 코드는 삭제됨)
    create_verification_code(db, email=req.email, code=code, expires_at=expires_at)
    
    # 5. 백그라운드 작업으로 이메일 전송
    background_tasks.add_task(send_verification_email, req.email, code)
    
    return {"msg": "이메일이 전송되었습니다. (가입된 이메일인 경우)"}


# 6) 비밀번호 초기화 (코드 검증)
# POST /users/password-reset/verify
@router.post("/password-reset/verify")
def verify_password_reset_code(
    req: PasswordResetVerify,
    db: Session = Depends(get_db)
):
    from app.crud.crud_verification import get_verification_code, check_verification_code_validity
    
    # 1. DB에서 인증 코드 조회
    v_code = get_verification_code(db, email=req.email, code=req.code)
    
    # 2. 코드 유효성 검증
    if not check_verification_code_validity(v_code):
        raise HTTPException(status_code=400, detail="유효하지 않거나 만료된 인증 코드입니다.")
        
    return {"msg": "인증 코드가 확인되었습니다. 새 비밀번호를 설정할 수 있습니다."}


# 7) 비밀번호 초기화 (새 비밀번호 설정)
# POST /users/password-reset/reset
@router.post("/password-reset/reset")
def reset_password(
    req: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    from app.crud.crud_verification import get_verification_code, check_verification_code_validity, delete_verification_codes_by_email
    from app.crud.crud_user import get_user_by_email
    from app.core.security import get_password_hash
    
    # 1. 코드 재검증 로직 (이메일 및 코드가 유효한지 다시 확인)
    v_code = get_verification_code(db, email=req.email, code=req.code)
    if not check_verification_code_validity(v_code):
        raise HTTPException(status_code=400, detail="유효하지 않거나 만료된 인증 코드입니다.")
        
    # 2. 사용자 조회
    user = get_user_by_email(db, email=req.email)
    if not user:
         raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
         
    # 3. 비밀번호 업데이트
    user.hashed_password = get_password_hash(req.new_password)
    db.add(user)
    
    # 4. 사용된 인증 코드 삭제
    delete_verification_codes_by_email(db, email=req.email)
    
    db.commit()
    return {"msg": "비밀번호가 성공적으로 변경되었습니다."}
