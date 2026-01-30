from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependency(의존성) 함수.
    API 요청 하나당 DB 세션을 열고, 요청이 끝나면 반드시 닫습니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()