from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

# 1. 기본 설계도 (공통으로 쓰는 필드)
class PostBase(SQLModel):
    title: str
    content: str
    author: str  # 나중에는 로그인한 유저 ID로 바꿀 예정

# 2. 실제 DB 테이블 (table=True)
class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    view_count: int = Field(default=0)

# 3. 데이터 생성용 (API 요청 받을 때 id, date는 입력 안 받음)
class PostCreate(PostBase):
    pass

# 4. 데이터 조회용 (API 응답 줄 때 id, date 포함)
class PostRead(PostBase):
    id: int
    created_at: datetime
    view_count: int