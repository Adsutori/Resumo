from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string
import logging

logger = logging.getLogger(__name__)

def send_verification_email(user):
    code = ''.join(random.choices(string.digits, k=6))
    user.verification_code = code
    user.verification_code_expires = timezone.now() + timedelta(minutes=15)
    user.save(update_fields=['verification_code', 'verification_code_expires'])

    try:
        send_mail(
            subject='Aktywuj swoje konto w Resumo!',
            message=f'Twój kod weryfikacyjny: \n\n{code}\n\nKod wygaśnie w ciągu 15 minut.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    except Exception as e:
        logger.error(f'Błąd wysyłania maila do {user.email}: {e}')
