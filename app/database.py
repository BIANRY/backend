from sqlmodel import SQLModel, create_engine, Session

# 1. DB 파일 이름 (프로젝트 루트에 생성됨)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. 엔진 생성 (connect_args는 SQLite 전용 설정)
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

# 3. 테이블 생성 함수 (앱 시작 시 실행)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 4. 세션 생성 함수 (Dependency로 사용)
def get_session():
    with Session(engine) as session:
        yield session