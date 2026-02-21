from datetime import datetime, timezone, timedelta
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

    # 3시간 쿨타임 로직 점검
    now = datetime.now(timezone.utc)
    if user.last_grass_sync is not None:
        # User 모델에 timezone=True 설정이 없다면 offset-naive할 수 있으므로 강제 세팅
        last_sync = user.last_grass_sync.replace(tzinfo=timezone.utc) if user.last_grass_sync.tzinfo is None else user.last_grass_sync
        if now - last_sync < timedelta(hours=3):
            raise HTTPException(
                status_code=429, 
                detail="최근 동기화 후 3시간이 지나야 새롭게 동기화할 수 있습니다."
            )

    # 크롤링 및 DB Upsert 호출
    synced_count = crud_grass.sync_user_grass(db, user)
    
    # 동기화 시간 갱신
    user.last_grass_sync = now
    db.commit()
    
    if synced_count == 0:
        return {"message": "잔디 데이터를 가져오지 못했거나 이미 최신 상태입니다.", "synced_days": 0}

    return {"message": "백준 잔디 데이터 동기화 완료", "synced_days": synced_count}


@router.get("/ranking", response_model=list[schemas_grass.RankingResponse])
def get_grass_ranking(
    year: int = Query(..., description="조회할 연도 (예: 2026)"),
    month: int = Query(..., description="조회할 월 (예: 2)"),
    db: Session = Depends(deps.get_db),
):
    """
    특정 연월의 백준 잔디 활동 순위(문제를 푼 날짜 수 기준)를 조회합니다.
    """
    ranking_data = crud_grass.get_monthly_ranking(db, year=year, month=month)
    return ranking_data
