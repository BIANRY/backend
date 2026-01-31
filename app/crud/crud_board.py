from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


class CRUDBoard(CRUDBase[Board, BoardCreate, BoardUpdate]):

    # 게시글 생성 (작성자 ID 포함)
    def create_with_owner(
            self, db: Session, *, obj_in: BoardCreate, user_id: int
    ) -> Board:
        obj_in_data = obj_in.model_dump()
        db_obj = Board(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # [수정됨] 목록 조회 (페이지네이션 지원용)
    # Router에서 page를 받아서 skip = (page - 1) * limit 계산 후 넘겨주면 됩니다.
    def get_multi_with_owner_check(
            self, db: Session, *, skip: int = 0, limit: int = 10, user_id: Optional[int] = None
    ) -> List[Board]:
        query = db.query(self.model)
        if user_id:
            query = query.filter(Board.user_id == user_id)

        # 최신글 순으로 정렬 (내림차순)
        return query.order_by(Board.id.desc()).offset(skip).limit(limit).all()


board = CRUDBoard(Board)