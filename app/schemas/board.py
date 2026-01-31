from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# --- 1. 작성자 정보 (Nested Schema) ---
# 게시글 정보에 작성자 이름만 포함하기 위한 미니 스키마
class BoardAuthor(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

# --- 2. 기본/생성/수정 스키마 ---
class BoardBase(BaseModel):
    title: str
    # 설계도 POST 요청에는 '제목, 본문'만 있지만,
    # DB 모델의 category가 not null이므로 포함해야 에러가 안 납니다.
    # (기본값을 주거나 프론트에서 받아야 함)
    category: str = "자유"

class BoardCreate(BoardBase):
    content: str  # 생성 시 본문 필수

class BoardUpdate(BaseModel):
    # 설계도 PUT 요청: [글 ID, 바꿀 제목, 바꿀 내용]
    # 카테고리는 수정 항목에 없으므로 제외
    title: Optional[str] = None
    content: Optional[str] = None

# --- 3. 응답(Response) 스키마 ---

# 공통 응답 필드 (ID, 작성자, 작성일, 카테고리)
class BoardResponseBase(BoardBase):
    id: int
    created_at: datetime
    # DB의 user 관계(relationship)를 통해 name을 가져옵니다.
    user: BoardAuthor = Field(alias="author")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True # author라는 별칭으로 데이터 내보내기 허용
    )

# [GET /board] 목록 조회용 (본문 제외)
class BoardListResponse(BoardResponseBase):
    pass

# [GET /board/{id}] 상세 조회용 (본문 포함)
class BoardDetailResponse(BoardResponseBase):
    content: str