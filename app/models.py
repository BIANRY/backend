from typing import Optional, List
from datetime import datetime, date

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


# 1. 사용자 모델
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    name: str
    student_id: str
    generation: int  # 기수
    role: str = "member"  # 기본값은 member
    baekjoon_id: Optional[str] = None  # 백준 ID (크롤링용)

    # 관계 설정 (User가 지워지면 작성글, 잔디정보도 같이 관리하기 위함)
    posts: List["Board"] = Relationship(back_populates="author")
    grasses: List["Grass"] = Relationship(back_populates="user")


# 2. 게시판 모델
class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Foreign Key (작성자)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    author: Optional[User] = Relationship(back_populates="posts")


# 3. 잔디심기(활동) 모델
class Grass(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("user_id", "date", name="unique_user_date"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    date: date  # YYYY-MM-DD
    solved_count: int  # 그날 푼 문제 수

    # Foreign Key (누구 기록인지)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="grasses")