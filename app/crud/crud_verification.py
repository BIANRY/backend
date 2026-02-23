from typing import Optional
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.verification_code import VerificationCode


def create_verification_code(db: Session, email: str, code: str, expires_at: datetime) -> VerificationCode:
    """새로운 인증 코드를 데이터베이스에 저장합니다."""
    # 같은 이메일로 이미 존재하는 코드가 있다면 삭제 (가장 최근 것만 유지)
    delete_verification_codes_by_email(db, email)

    db_obj = VerificationCode(
        email=email,
        code=code,
        expires_at=expires_at
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_verification_code(db: Session, email: str, code: str) -> Optional[VerificationCode]:
    """주어진 이메일과 코드로 인증 코드 레코드를 조회합니다."""
    stmt = select(VerificationCode).where(
        VerificationCode.email == email,
        VerificationCode.code == code
    )
    return db.execute(stmt).scalar_one_or_none()


def delete_verification_codes_by_email(db: Session, email: str) -> None:
    """주어진 이메일에 해당하는 모든 인증 코드 레코드를 삭제합니다."""
    stmt = select(VerificationCode).where(VerificationCode.email == email)
    existing_codes = db.execute(stmt).scalars().all()
    for existing_code in existing_codes:
        db.delete(existing_code)
    db.commit()


def check_verification_code_validity(verification_code: Optional[VerificationCode]) -> bool:
    """인증 코드가 유효한지(존재하고 만료되지 않았는지) 확인합니다."""
    if not verification_code:
        return False

    # datetime에 timezone이 없다면 UTC로 가정
    now = datetime.now(timezone.utc)
    expires_at = verification_code.expires_at

    # Naive vs Aware datetime 처리 방어 로직
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if now > expires_at:
        return False

    return True
