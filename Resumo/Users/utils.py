from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string


def send_verification_email(user):
    code = ''.join(random.choices(string.digits, k=6))
    user.verification_code = code
    user.verification_code_expires = timezone.now() + timedelta(minutes=15)
    user.save()

    send_mail(
        subject='Activate your PocketUp account!',
        message=f'Your verification code: \n\n{code}\n\nThe code will expire in 15 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )