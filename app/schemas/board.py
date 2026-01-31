from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class BoardCreate(BaseModel):
    title: str
    content: str
    category: str


class BoardUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class BoardAuthor(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class BoardResponseBase(BaseModel):
    id: int
    title: str
    category: str
    user: BoardAuthor
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardListResponse(BaseModel):
    total: int
    question_list: list[BoardResponseBase] = []


class BoardDetailResponse(BoardResponseBase):
    content: str
