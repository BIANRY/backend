from typing import List

from pydantic import BaseModel, ConfigDict


class RankingResponse(BaseModel):
    user_id: int
    name: str
    baekjoon_id: str | None
    monthly_active_days: int

    model_config = ConfigDict(from_attributes=True)


class GrassSyncResponse(BaseModel):
    message: str
    synced_days: int
