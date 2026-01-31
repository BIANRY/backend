from typing import Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


# from app.core.security import get_password_hash  # 추후 보안 파일 만들 때 주석 해제

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # 1. 일반적인 딕셔너리로 변환
        create_data = obj_in.model_dump()

        # 2. 비밀번호 분리 및 해싱 (보안 기능 구현 전이면 임시로 그냥 저장)
        # password = create_data.pop("password")
        # create_data["hashed_password"] = get_password_hash(password)

        # 지금은 해싱 로직 없이 예시로 작성 (나중에 위 주석 코드로 교체!)
        password = create_data.pop("password")
        create_data["hashed_password"] = password + "_hashed_secret"

        db_obj = User(**create_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)