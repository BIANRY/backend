from typing import Optional
from datetime import date
from pydantic import BaseModel

# 1. 공통
class GrassBase(BaseModel):
    date: date
    solved_count: int

# 2. 생성
class GrassCreate(GrassBase):
    pass

# 3. 수정
class GrassUpdate(BaseModel):
    solved_count: Optional[int] = None

# 4. 응답
class GrassResponse(GrassBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True