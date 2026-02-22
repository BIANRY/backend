from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


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
