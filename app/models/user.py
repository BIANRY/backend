from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Column(Integer, primary_key=True, index=True)
    email: Column(String, unique=True, index=True, nullable=False)
    hashed_password: Column(String, nullable=False)
    name : Column(String, nullable=False)
    student_id: Column(Integer, unique=True, index=True, nullable=False)
    generation: Column(Integer, nullable=False)
    role: Column(String, default="member")
    baekjoon_id: Column(String)

    boards = relationship("Board", back_populates="user")
    grasses = relationship("Grass", back_populates="user")
