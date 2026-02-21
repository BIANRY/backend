from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    student_id = Column(String(10), unique=True, nullable=False)
    # generation = Column(Integer, nullable=False)
    role = Column(String(255), default="member")
    baekjoon_id = Column(String(255))
    tier = Column(Integer, default=0)
    last_grass_sync = Column(DateTime(timezone=True), nullable=True)

    boards = relationship("Board", back_populates="user")
    grasses = relationship("Grass", back_populates="user")
