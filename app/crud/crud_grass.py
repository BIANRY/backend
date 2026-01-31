from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.grass import Grass
from app.schemas.grass import GrassCreate, GrassUpdate


class CRUDGrass(CRUDBase[Grass, GrassCreate, GrassUpdate]):

    def create_with_owner(
            self, db: Session, *, obj_in: GrassCreate, user_id: int
    ) -> Grass:
        obj_in_data = obj_in.model_dump()
        db_obj = Grass(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # 특정 사용자의 모든 잔디 조회
    def get_by_user(self, db: Session, *, user_id: int) -> List[Grass]:
        return db.query(Grass).filter(Grass.user_id == user_id).all()


grass = CRUDGrass(Grass)