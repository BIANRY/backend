from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables

# 라우터 가져오기
from app.routers import auth, board, grass, users

app = FastAPI(
    title="동아리 홈페이지 API",
    description="겨울방학 프로젝트 백엔드 API 문서입니다.",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 포트 3000, 5500 등 허용)
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

# 앱 시작 시 DB 테이블 자동 생성
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 라우터 등록
# app.include_router(auth.router)
# app.include_router(users.router)
# app.include_router(board.router)
# app.include_router(activity.router)

@app.get("/")
def read_root():
    return {"message": "Hello World! 동아리 프로젝트 API 서버입니다."}