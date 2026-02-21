from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import curd_grass as crud_grass
from app.crud import crud_user
from app.schemas import grass as schemas_grass

router = APIRouter()


@router.post("/sync/{student_id}", response_model=schemas_grass.GrassSyncResponse)
def sync_grass(
    student_id: str,
    db: Session = Depends(deps.get_db),
    # current_user = Depends(deps.get_current_active_user)
):
    """
    특정 사용자의 백준 잔디 데이터를 가져와 DB와 동기화합니다.
    """
    user = crud_user.get_user(db, student_id=student_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not user.baekjoon_id:
        raise HTTPException(status_code=400, detail="이 사용자는 백준 아이디가 등록되어 있지 않습니다.")

    # 크롤링 및 DB Upsert 호출
    synced_count = crud_grass.sync_user_grass(db, user)
    
    if synced_count == 0:
        return {"message": "잔디 데이터를 가져오지 못했거나 이미 최신 상태입니다.", "synced_days": 0}

    return {"message": "백준 잔디 데이터 동기화 완료", "synced_days": synced_count}


@router.get("/ranking", response_model=list[schemas_grass.RankingResponse])
def get_grass_ranking(
    year: int = Query(..., description="조회할 연도 (예: 2025)"),
    month: int = Query(..., description="조회할 월 (예: 2)"),
    db: Session = Depends(deps.get_db),
):
    """
    특정 연월의 백준 잔디 활동 순위(문제를 푼 날짜 수 기준)를 조회합니다.
    """
    ranking_data = crud_grass.get_monthly_ranking(db, year=year, month=month)
    return ranking_data
