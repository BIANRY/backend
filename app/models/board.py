from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Board(Base):
    __tablename__ = "boards"

    id: Column(Integer, primary_key=True, index=True)
    title: Column(String, nullable=False)
    content: Column(String, nullable=False)
    category: Column(String, nullable=False)
    created_at: Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="boards")
