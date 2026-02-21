from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.grass import Grass
from app.models.user import User
from app.core.baekjoon import fetch_baekjoon_grass, fetch_solvedac_tier


def sync_user_grass(db: Session, user: User) -> int:
    """
    유저의 백준 잔디 기록과 solved.ac 티어 정보를 크롤링하여 테이블에 Upsert 및 업데이트합니다.
    """
    if not user.baekjoon_id:
        return 0

    # 1. 티어 정보 갱신
    tier = fetch_solvedac_tier(user.baekjoon_id)
    user.tier = tier

    # 2. 잔디 정보 갱신
    grass_data = fetch_baekjoon_grass(user.baekjoon_id)
    if not grass_data:
        db.commit() # 티어라도 반영
        return 0

    stmt = insert(Grass).values([
        {
            "user_id": user.id,
            "date": g["date"],
            "solved_count": g["solved_count"]
        }
        for g in grass_data
    ])
    
    stmt = stmt.on_conflict_do_update(
        constraint="unique_user_date",
        set_={"solved_count": stmt.excluded.solved_count}
    )
    
    db.execute(stmt)
    db.commit()
    
    return len(grass_data)


def get_monthly_ranking(db: Session, year: int, month: int):
    """
    특정 연/월의 "문제를 푼 날짜 수(attendance)" 와 "현재(어제/오늘 기준) 연속 풀이 일수(streak)"를 계산하여 순위를 매깁니다.
    """
    from datetime import datetime, timedelta, timezone

    # 대한민국(KST) 시간대 기준으로 오늘 날짜 판단
    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST).date()
    yesterday = today - timedelta(days=1)

    # 1. 해당 연월에 1번이라도 문제를 푼 대상 회원 목록과 월 출석일수 획득
    attendance_records = (
        db.query(
            User.id, 
            User.name, 
            User.baekjoon_id, 
            User.tier, 
            func.count(Grass.id).label("attendance")
        )
        .join(Grass, (User.id == Grass.user_id) & 
                     (func.extract('year', Grass.date) == year) & 
                     (func.extract('month', Grass.date) == month) &
                     (Grass.solved_count > 0))
        .group_by(User.id)
        .all()
    )

    if not attendance_records:
        return []

    target_user_ids = [r.id for r in attendance_records]

    # 2. 대상 유저들의 전체 잔디 기록을 최신 Date 내림차순으로 가져와서 "현재 진행 중인" Streak 탐색
    all_grass = (
        db.query(Grass.user_id, Grass.date)
        .filter(Grass.user_id.in_(target_user_ids), Grass.solved_count > 0)
        .order_by(Grass.user_id, Grass.date.desc())
        .all()
    )

    user_dates = {}
    for gid, gdate in all_grass:
        if gid not in user_dates:
            user_dates[gid] = []
        user_dates[gid].append(gdate)

    ranking = []
    
    for r in attendance_records:
        uid = r.id
        dates = user_dates.get(uid, [])
        
        current_streak = 0
        if dates:
            first_date = dates[0]
            # 최근 풀이일이 오늘이거나 어제인 경우에만 연속 출석으로 인정
            if first_date == today or first_date == yesterday:
                current_streak = 1
                for i in range(1, len(dates)):
                    expected_date = dates[i-1] - timedelta(days=1)
                    if dates[i] == expected_date:
                        current_streak += 1
                    else:
                        break
                        
        ranking.append({
            "user_id": uid,
            "name": r.name,
            "baekjoon_id": r.baekjoon_id,
            "tier": r.tier or 0,
            "attendance": r.attendance,
            "streak": current_streak
        })
        
    # 3. 정렬 기준 
    # 1순위: 출석일수(attendance) DESC
    # 2순위: 스트릭(streak) DESC
    # 3순위: 티어(tier) DESC
    # 4순위: 이름(name) ASC
    ranking.sort(key=lambda x: (-x['attendance'], -x['streak'], -x['tier'], x['name']))
    
    return ranking
