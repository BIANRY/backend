from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.grass import Grass
from app.models.user import User
from app.core.baekjoon import fetch_baekjoon_grass


def sync_user_grass(db: Session, user: User) -> int:
    """
    유저의 백준 잔디 기록을 크롤링하여 Grass 테이블에 Upsert 합니다.
    """
    if not user.baekjoon_id:
        return 0

    grass_data = fetch_baekjoon_grass(user.baekjoon_id)
    if not grass_data:
        return 0

    # PostgreSQL의 INSERT ON CONFLICT DO UPDATE 기능을 활용한 빠르고 안전한 Upsert
    stmt = insert(Grass).values([
        {
            "user_id": user.id,
            "date": g["date"],
            "solved_count": g["solved_count"]
        }
        for g in grass_data
    ])
    
    # 중복 키 (user_id, date) 발생 시 solved_count를 최신으로 업데이트
    stmt = stmt.on_conflict_do_update(
        constraint="unique_user_date",
        set_={"solved_count": stmt.excluded.solved_count}
    )
    
    db.execute(stmt)
    db.commit()
    
    return len(grass_data)


def get_monthly_ranking(db: Session, year: int, month: int):
    """
    특정 연/월 동안 "문제를 푼 날짜 수"를 기준으로 순위를 매깁니다.
    """
    # 1. 월별로 푼 일수(solved_count > 0 인 레코드 수)를 계산하는 SubQuery/Query
    ranking = (
        db.query(
            User.id.label("user_id"),
            User.name,
            User.baekjoon_id,
            func.count(Grass.id).label("monthly_active_days")
        )
        .join(Grass, (User.id == Grass.user_id) &
                     (func.extract('year', Grass.date) == year) &
                     (func.extract('month', Grass.date) == month) &
                     (Grass.solved_count > 0))
        .group_by(User.id)
        .order_by(func.count(Grass.id).desc(), User.name.asc()) # 푼 일수 내림차순, 이름 오름차순
        .all()
    )
    
    return ranking
