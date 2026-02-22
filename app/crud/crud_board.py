from sqlalchemy.orm import Session

from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


def get_board_list(db: Session, skip: int = 0, limit: int = 10):
    _board_list = db.query(Board).order_by(Board.created_at.desc())

    total = _board_list.count()
    board_list = _board_list.offset(skip).limit(limit).all()

    return total, board_list


def get_board(db: Session, board_id: int):
    board = db.query(Board).filter(Board.id == board_id).first()

    return board


def create_board(db: Session, board_create: BoardCreate):
    db_board = Board(
        title=board_create.title,
        content=board_create.content,
        category=board_create.category,
        user_id=board_create.user_id
    )
    db.add(db_board)
    db.commit()


def update_board(db: Session, db_board: Board, board_update: BoardUpdate):
    db_board.title = board_update.title
    db_board.content = board_update.content
    db.add(db_board)
    db.commit()


def delete_board(db: Session, db_board: Board):
    db.delete(db_board)
    db.commit()
