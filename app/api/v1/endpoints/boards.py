from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.crud_board import get_board_list, create_board, get_board, update_board, delete_board
from app.schemas.board import BoardListResponse, BoardCreate, BoardDetailResponse, BoardUpdate

router = APIRouter()

# 1️⃣ 게시판 목록 조회
# GET /board?page=1
@router.get("", response_model=BoardListResponse)
def board_list(
    page: int = 1,
    db: Session = Depends(get_db),
):
    limit = 10
    skip = (page - 1) * limit

    total, boards = get_board_list(db, skip=skip, limit=limit)

    return {
        "total": total,
        "question_list": boards,
    }


# 2️⃣ 게시글 작성
# POST /board
@router.post("")
def board_create(
    _board_create: BoardCreate,
    db: Session = Depends(get_db),
):
    create_board(db, _board_create)


# 3️⃣ 게시글 상세 조회
# GET /board/{id}
@router.get("/{id}", response_model=BoardDetailResponse)
def board_detail(
    id: int,
    db: Session = Depends(get_db),
):
    board = get_board(db, board_id=id)

    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    return board


# 4️⃣ 게시글 수정
# PUT /board/{id}
@router.put("/{id}")
def board_update(
    id: int,
    board_update: BoardUpdate,
    db: Session = Depends(get_db),
):
    board = get_board(db, board_id=id)

    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    update_board(db, board, board_update)


# 5️⃣ 게시글 삭제
# DELETE /board/{id}
@router.delete("/{id}")
def board_delete(
    id: int,
    db: Session = Depends(get_db),
):
    board = get_board(db, board_id=id)

    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    delete_board(db, board)
