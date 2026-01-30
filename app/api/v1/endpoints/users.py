from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db

router = APIRouter()

@router.get("/users/")
def read_users(db: Session = Depends(get_db)):
    # db 변수는 이제 MySQL과 연결된 세션 객체입니다.
    # users = db.query(User).all()
    # return users
    return {"message": "MySQL DB connected!"}