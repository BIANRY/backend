# 🦁 BINARY 홈페이지 겨울방학 프로젝트 (Backend)

이 프로젝트는 우리 동아리 홈페이지의 **백엔드 API 서버**입니다.  
**FastAPI**와 **SQLModel**을 사용하여 만들어졌습니다.

개발이 처음이라도 괜찮습니다! 아래 가이드를 따라 천천히 실행해 보세요.

---

## 🛠 1. 필수 준비물 (Prerequisites)

시작하기 전에 컴퓨터에 아래 프로그램들이 설치되어 있어야 합니다.

1.  **Python (3.10 이상)**: [다운로드 링크](https://www.python.org/downloads/)
    * *설치할 때 `Add Python to PATH` 체크박스를 꼭 체크해주세요!*
2.  **VS Code**: [다운로드 링크](https://code.visualstudio.com/)
3.  **Git**: [다운로드 링크](https://git-scm.com/)

---

## 🚀 2. 설치 및 실행 방법 (Installation)

명령 프롬프트(cmd), 파워쉘(PowerShell), 혹은 VS Code의 터미널을 열고 따라 하세요.

### Step 1. 프로젝트 다운로드 (Clone)
```bash
git clone https://github.com/BIANRY/backend.git
cd backend
```

### Step 2. 가상환경(Virtual Environment) 만들기

파이썬 라이브러리들이 뒤섞이지 않게 우리만의 방(가상환경)을 만듭니다.

**💻 윈도우 (Windows) 사용자:**

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 실행 (터미널 앞쪽에 (venv)가 생기면 성공!)
venv\Scripts\activate
```

**🍎 맥(Mac) / 리눅스 사용자:**

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 실행 (터미널 앞쪽에 (venv)가 생기면 성공!)
source venv/bin/activate
```

### Step 3. 라이브러리 설치

방(가상환경)에 들어왔으니 필요한 가구(라이브러리)를 배치합니다.

```bash
pip install -r requirements.txt
```

### Step 4. 서버 실행 🏃

설치가 끝났습니다! 이제 서버를 켜봅시다.

```bash
uvicorn app.main:app --reload
```

* `Application startup complete.` 라는 메시지가 뜨면 성공입니다.
* `--reload` 옵션은 코드를 저장할 때마다 서버를 자동으로 재시작해줍니다.

---

## 📚 3. API 문서 확인하기 (Swagger UI)

서버가 켜진 상태에서 인터넷 브라우저를 열고 아래 주소로 들어가세요.

👉 **http://127.0.0.1:8000/docs**

* 여기서 우리가 만든 API 목록을 볼 수 있습니다.
* `Try it out` -> `Execute` 버튼을 누르면 실제로 데이터를 주고받을 수 있습니다.
* 프론트엔드 팀원들은 이 페이지를 보고 개발하면 됩니다.

---

## 📂 4. 프로젝트 구조 (어디를 고쳐야 하나요?)

```text
app/
├── main.py            # ⚙️ 설정 파일 (건들지 마세요!)
├── database.py        # 🗄️ DB 연결 파일
├── models.py          # 📝 데이터 설계도 (여기에 테이블을 정의합니다)
└── routers/           # 🚦 실제 기능 구현 (여러분이 작업할 곳!)
    ├── auth.py        # 로그인 관련
    ├── board.py       # 게시판 기능 (예시)
    └── grass.py       # [미션] 잔디심기 기능 구현하기
```

### 💡 Backend 어시스턴트 팁

* 새로운 기능을 만들 때는 `routers/` 폴더 안에 파일을 만듭니다.
* 데이터베이스에 저장할 내용이 바뀌면 `models.py`를 수정합니다.

---

## ⚠️ 5. 주의사항 (Troubleshooting)

1. **`command not found: python` 에러가 나요!**
   * 맥 사용자는 `python` 대신 `python3`라고 입력해 보세요.
   * 윈도우 사용자는 파이썬 설치 시 `PATH` 설정을 안 했을 수 있습니다. 재설치해주세요.
2. **`Scripts/activate` 보안 오류가 나요! (윈도우)**
   * 파워쉘에서 `Set-ExecutionPolicy Unrestricted` 를 입력하거나, `cmd` 창을 사용하세요.
3. **Git Push가 안 돼요!**
   * 다른 친구가 먼저 코드를 올렸을 수 있습니다. `git pull`을 먼저 하고 다시 시도하세요.