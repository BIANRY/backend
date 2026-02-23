import resend
from app.core.config import settings

def send_verification_email(to_email: str, code: str):
    """
    비밀번호 인증 코드를 Resend API를 통해 이메일로 전송합니다.
    """
    if not settings.RESEND_API_KEY:
        print(f"[{to_email}] Resend API 키가 설정되지 않아 이메일을 발송하지 않습니다. 인증 코드: {code}")
        return

    resend.api_key = settings.RESEND_API_KEY
    
    html_content = f"""
    <p>안녕하세요.</p>
    <p>비밀번호 초기화를 위한 인증 코드입니다.</p>
    <p>아래의 인증 코드를 홈페이지에 입력해주세요.</p>
    <h2>{code}</h2>
    <p>이 코드는 5분 후 만료됩니다.</p>
    """

    params = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": "[BINARY] 비밀번호 초기화 인증 코드",
        "html": html_content,
    }

    try:
        response = resend.Emails.send(params)
        print(f"[{to_email}] 비밀번호 인증 이메일을 발송했습니다. (Resend API)")
    except Exception as e:
        print(f"[{to_email}] 이메일 발송 중 오류 발생: {e}")

