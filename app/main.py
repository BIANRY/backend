from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("앱을 시작합니다.")

    yield

    print("앱을 종료합니다.")

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        lifespan=lifespan
    )

    # CORS (Cross-Origin Resource Sharing) 설정
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 배포시 특정 도메인만 설정
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터 등록
    # application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = get_application()


# 헬스 체크용 기본 엔드포인트
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!", "env": settings.PROJECT_NAME}


# 디버깅 용: python app/main.py 로 직접 실행할 때만 작동
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)