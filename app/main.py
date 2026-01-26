from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables

# 1. Lifespan (수명 주기) 정의
# 서버가 시작되기 전과 종료된 후에 실행될 로직을 정의합니다.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # [시작 전 실행] DB 테이블 만들기
    print("🚀 서버 시작! 데이터베이스 테이블을 생성합니다...")
    create_db_and_tables()

    yield  # 이 시점에서 서버가 동작합니다 (요청을 받음)

    # [종료 후 실행]
    print("👋 서버 종료! 리소스를 정리합니다.")


# 2. FastAPI 앱 생성 (lifespan 파라미터 추가)
app = FastAPI(
    title="동아리 프로젝트 API",
    description="겨울방학 프로젝트 백엔드 API 문서입니다.",
    version="1.0.0",
    lifespan=lifespan  # 여기에 위에서 만든 함수를 넣어줍니다.
)

# 3. CORS 설정
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
# app.include_router(auth.router)
# app.include_router(users.router)
# app.include_router(board.router)
# app.include_router(activity.router)

@app.get("/")
def read_root():
    return {"message": "Hello World! BINARY 프로젝트 API 서버입니다."}