import resend
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_verification_email(user):
    try:
        resend.api_key = settings.RESEND_API_KEY

        resend.Emails.send({
            "from": "Resumo <onboarding@resend.dev>",
            "to": [user.email],
            "subject": "Aktywuj swoje konto w Resumo!",
            "html": f"""
                <h2>Witaj, {user.first_name}!</h2>
                <p>Twój kod weryfikacyjny to:</p>
                <h1 style="letter-spacing: 8px;">{user.verification_code}</h1>
                <p>Kod jest ważny przez 24 godziny.</p>
            """,
        })
    except Exception as e:
        logger.error(f"[EMAIL ERROR] {type(e).__name__}: {e}")
        raise  # re-raise żeby 500 dalej się pokazał, ale błąd trafi do logów
