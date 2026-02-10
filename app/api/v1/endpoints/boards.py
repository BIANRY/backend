from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import crud_board
from app.schemas.board import BoardListResponse

router = APIRouter()

@router.get("/", response_model=BoardListResponse)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10):
    total, _question_list = crud_board.get_board_list(db, skip=page * size, limit=size)

    return {
        "total": total,
        'question_list': _question_list
    }
