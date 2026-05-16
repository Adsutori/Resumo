import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

def send_verification_email(user):
    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": settings.BREVO_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "sender": {"name": "Resumo", "email": "kajotpl@outlook.com"},
                "to": [{"email": user.email}],
                "subject": "Aktywuj swoje konto w Resumo!",
                "htmlContent": f"""
                    <h2>Witaj, {user.first_name}!</h2>
                    <p>Twój kod weryfikacyjny to:</p>
                    <h1 style="letter-spacing: 8px;">{user.verification_code}</h1>
                    <p>Kod jest ważny przez 24 godziny.</p>
                """,
            },
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"[EMAIL ERROR] {type(e).__name__}: {e}")
        raise
