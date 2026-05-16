import resend
from django.conf import settings

def send_verification_email(user):
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
