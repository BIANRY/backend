# 🦁 BINARY 홈페이지 프로젝트 (Backend)

이 프로젝트는 **BINARY 동아리 홈페이지의 백엔드 API 서버**입니다.  
최신 파이썬 웹 프레임워크인 **FastAPI**와 **SQLAlchemy/SQLModel**을 활용하여 구축되었으며, 빠르고 안정적인 RESTful API를 제공합니다.

---

## 🛠 1. 기술 스택 (Tech Stack)

### Core
*   **Language:** Python 3.10+
*   **Web Framework:** FastAPI
*   **ASGI Server:** Uvicorn

### Database & ORM
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy / SQLModel
*   **Migration:** Alembic

### Security & Authentication
*   **Validation:** Pydantic
*   **Authentication:** JWT (JSON Web Token) via `pyjwt`, `python-jose`
*   **Password Hashing:** Argon2 via `pwdlib[argon2]`

---

## 🚀 2. 시작하기 (Getting Started)

### 사전 준비 (Prerequisites)
*   [Python 3.10 이상](https://www.python.org/downloads/) 설치
*   Git 설치
*   PostgreSQL 설치 및 실행 (로컬 환경 기준)

### 로컬 개발 환경 세팅 (Installation)

1. **프로젝트 클론 (Clone Repository)**
   ```bash
   git clone https://github.com/BIANRY/backend.git
   cd backend
   ```

2. **가상환경 생성 및 활성화 (Virtual Environment)**
   * **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **패키지 설치 (Install Dependencies)**
   ```bash
   pip install -r requirements.txt
   ```

4. **환경 변수 설정 (Environment Variables)**
   * 프로젝트 루트 디렉토리에 `.env` 파일을 복사하거나 생성합니다.
   * 필요한 데이터베이스 연결 정보 및 JWT Secret Key 등을 설정합니다.

5. **데이터베이스 마이그레이션 (Database Migration)**
   * 테이블 스키마를 최신 상태로 설정합니다.
   ```bash
   alembic upgrade head
   ```

6. **서버 실행 (Run Server)**
   ```bash
   uvicorn app.main:app --reload
   ```
   * 서버가 정상적으로 실행되면 **http://127.0.0.1:8000** 에서 API에 접근할 수 있습니다.

---

## 📚 3. API 문서 확인 (Swagger UI)

FastAPI는 자동으로 대화형 API 문서를 생성합니다.
서버를 실행한 후, 브라우저에서 아래 주소에 접속하여 API를 실시간으로 테스트해 볼 수 있습니다.

👉 **Swagger UI:** [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)  
👉 **ReDoc:** [http://127.0.0.1:8000/api/v1/redoc](http://127.0.0.1:8000/api/v1/redoc)

---

## 📂 4. 프로젝트 구조 (Project Structure)

체계적인 개발 및 유지보수를 위해 계층형 아키텍처(Layered Architecture)를 따르고 있습니다.

```text
app/
├── api/               # API 엔드포인트 세부 로직 (라우터)
│   ├── deps.py        # 의존성 주입 (DB 세션, User 인증 등)
│   └── v1/endpoints/  # API 버전별 상세 구현 (boards, users 등)
├── core/              # 공통 설정 (환경 변수, 보안 설정 등)
├── crud/              # CRUD 로직 (데이터베이스 질의 처리)
├── db/                # 데이터베이스 세션 및 연결 설정
├── models/            # 데이터베이스 테이블 스키마 정의 (SQLAlchemy)
├── schemas/           # API 데이터 유효성 검사 및 직렬화/역직렬화 (Pydantic)
└── main.py            # FastAPI 애플리케이션 진입점 및 CORS 설정
```

### 💡 주요 기능 요약
*   **인증 및 유저 관리 (users.py):** 회원가입, 로그인(JWT 발급) 및 사용자 정보 관리
*   **게시판 기능 (boards.py):** 게시글 생성, 조회, 수정, 삭제 처리
*   **잔디심기 기능 (grass.py):** 사용자의 활동 로그 혹은 잔디(활동 기여도) 시각화 기능 지원 개발 중

---

## ⚠️ 5. 주의사항 (Troubleshooting)

1. **`command not found: python`**
   * 맥(Mac) 사용자는 `python` 대신 `python3`를 입력하세요.

2. **가상환경 스크립트 실행 권한 오류 (Windows)**
   * PowerShell에서 관리자 권한으로 열고 `Set-ExecutionPolicy Unrestricted`를 입력하여 실행 권한을 허용해 주세요.

3. **데이터베이스 연결 오류**
   * `.env` 파일의 연결 정보(DB 주소, User, Password)가 정확한지, 그리고 실제 DB 서버가 켜져 있는지 확인하세요.