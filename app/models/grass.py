from sqlalchemy import UniqueConstraint, Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Grass(Base):
    __tablename__ = "grass"
    __table_args__ = (UniqueConstraint("user_id", "date", name="unique_user_date"),)

    id: Column(Integer, primary_key=True, index=True)
    date: Column(Date, nullable=False)
    solved_count: Column(Integer, nullable=False)

    user_id: Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="grasses")
