from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str
    API_V1_STR: str

    # 데이터베이스 설정 (기본값 설정 또는 필수값 지정)
    DATABASE_URL: str

    # 보안 관련 (JWT Secret Key 등)
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 이메일 전송 (SMTP) 설정
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""


    # .env 파일 로드 설정 (Pydantic v2 방식)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# 인스턴스 생성 (이 객체를 다른 파일에서 import 해서 사용)
settings = Settings()