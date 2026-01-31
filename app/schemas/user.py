from typing import Optional
from pydantic import BaseModel, EmailStr

# 1. 공통 속성 (읽기/쓰기 모두 사용)
class UserBase(BaseModel):
    email: EmailStr
    name: str
    student_id: int
    generation: int
    role: Optional[str] = "member"
    baekjoon_id: Optional[str] = None

# 2. 생성 시 필요한 속성 (비밀번호 필수!)
class UserCreate(UserBase):
    password: str

# 3. 업데이트 시 필요한 속성 (모든 필드가 옵션)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    student_id: Optional[int] = None
    generation: Optional[int] = None
    baekjoon_id: Optional[str] = None
    password: Optional[str] = None # 비밀번호 변경 시 사용

# 4. 조회(응답) 시 보여줄 속성 (비밀번호 제외, ID 포함)
class UserResponse(UserBase):
    id: int
    is_active: bool = True # 모델에 없으면 빼도 됨 (예시)

    # Pydantic v2 설정: ORM 객체(SQLAlchemy)를 Pydantic 모델로 변환 허용
    class Config:
        from_attributes = True