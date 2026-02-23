import smtplib
from email.message import EmailMessage
from app.core.config import settings

def send_verification_email(to_email: str, code: str):
    """
    비밀번호 인증 코드를 이메일로 전송합니다.
    """
    # 환경변수 확인
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"[{to_email}] SMTP 정보가 부족하여 이메일을 발송하지 않습니다. 인증 코드: {code}")
        return

    msg = EmailMessage()
    msg.set_content(
        f"안녕하세요.\n\n"
        f"비밀번호 초기화를 위한 인증 코드입니다.\n"
        f"아래의 인증 코드를 홈페이지에 입력해주세요.\n\n"
        f"인증 코드: {code}\n\n"
        f"이 코드는 5분 후 만료됩니다."
    )
    
    msg["Subject"] = "[BINARY] 비밀번호 초기화 인증 코드"
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[{to_email}] 비밀번호 인증 이메일을 발송했습니다.")
    except Exception as e:
        print(f"[{to_email}] 이메일 발송 중 오류 발생: {e}")
