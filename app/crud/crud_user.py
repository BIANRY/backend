from app.schemas.user import UserUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException

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


def update_user(db: Session, db_user: User, user_update: UserUpdate):
    from app.crud.curd_grass import sync_user_grass
    from app.models.grass import Grass

    update_data = user_update.model_dump(exclude_unset=True)

    # Handle password update separately
    if "new_password" in update_data:
        if "old_password" not in update_data or not update_data["old_password"]:
            raise HTTPException(status_code=400, detail="기존 비밀번호를 입력해주세요.")

        if not verify_password(update_data["old_password"], db_user.hashed_password):
            raise HTTPException(status_code=400, detail="기존 비밀번호가 일치하지 않습니다.")

        hashed_password = get_password_hash(update_data["new_password"])
        del update_data["new_password"]
        if "old_password" in update_data:
            del update_data["old_password"]
        update_data["hashed_password"] = hashed_password
    elif "old_password" in update_data:
        del update_data["old_password"]

    # Check if baekjoon_id is changing
    is_baekjoon_id_changed = False
    if "baekjoon_id" in update_data and update_data["baekjoon_id"] != db_user.baekjoon_id:
        is_baekjoon_id_changed = True

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    if is_baekjoon_id_changed:
        # Delete existing grass records for this user
        db.query(Grass).filter(Grass.user_id == db_user.id).delete()
        db_user.tier = 0
        db.commit()

        # Trigger sync for new ID
        if db_user.baekjoon_id:
            db.refresh(db_user)
            sync_user_grass(db, db_user)

    return db_user
