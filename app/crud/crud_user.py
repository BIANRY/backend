from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        name=user_create.name,
        student_id=user_create.student_id,
        email=user_create.email,
        hashed_password=pwd_context.hash(user_create.password)
    )
    db.add(db_user)
    db.commit()
