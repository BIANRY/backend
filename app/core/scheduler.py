import asyncio
from datetime import datetime, timezone
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.session import SessionLocal
from app.crud import curd_grass as crud_grass
from app.models.user import User


# 백그라운드 태스크 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 이벤트 루프에 연결할 Async 스케줄러 인스턴스
scheduler = AsyncIOScheduler()

def sync_all_users_grass_job():
    """
    DB에 있는 모든 유저의 잔디 데이터를 일괄 동기화하는 태스크.
    동기화 함수가 동기(sync) 함수이므로 자체 세션을 열어 처리합니다.
    """
    logger.info(f"[{datetime.now(timezone.utc)}] 일괄 잔디 동기화 스케줄러 시작")
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.baekjoon_id.isnot(None)).all()
        synced_count = 0
        
        for user in users:
            try:
                # 봇 차단을 방지하기 위해 각 유저별 1초 대기 (간헐적 처리)
                # 실제 async 환경에서는 db I/O 블로킹 방지를 위해 run_in_executor 가 권장되나
                # 단순 크론 스케줄이 목적이므로 간단히 작성
                import time
                time.sleep(1)
                
                added = crud_grass.sync_user_grass(db, user)
                if added > 0:
                    user.last_grass_sync = datetime.now(timezone.utc)
                    db.commit()
                synced_count += 1
            except Exception as e:
                logger.error(f"[User: {user.baekjoon_id}] 잔디 동기화 실패: {e}")
                db.rollback()
                
        logger.info(f"[{datetime.now(timezone.utc)}] 일괄 잔디 동기화 완료: {synced_count}명")
    except Exception as e:
        logger.error(f"스케줄러 전체 에러 발생: {e}")
    finally:
        db.close()


def setup_scheduler():
    # 매일 밤 12시 10분 (0시 10분) KST 기준 
    # (서버 환경에 따라 Timezone을 명시하거나 보정해야 할 수 있습니다. 
    # 기본적으로 서버 OS의 locale 시간을 따릅니다.)
    scheduler.add_job(
        sync_all_users_grass_job,
        'cron',
        hour=0,
        minute=10,
        id="sync_grass_daily",
        replace_existing=True
    )
    scheduler.start()
