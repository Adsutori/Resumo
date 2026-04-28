import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


def create_notification(user, type, title, message=''):
    """
    Tworzy powiadomienie dla usera.
    Nie tworzy duplikatów tego samego typu w ciągu 24h.
    """
    try:
        from .models import Notification
        from datetime import timedelta

        # Nie duplikuj tego samego powiadomienia w ciągu 24h
        recent_cutoff = timezone.now() - timedelta(hours=24)
        already_exists = Notification.objects.filter(
            user=user,
            type=type,
            title=title,
            created_at__gte=recent_cutoff,
        ).exists()

        if already_exists:
            return None

        return Notification.objects.create(
            user=user,
            type=type,
            title=title,
            message=message,
        )
    except Exception as e:
        logger.warning(f'create_notification failed: {e}')
        return None


def notify_welcome(user):
    create_notification(
        user=user,
        type='welcome',
        title=f'Witaj w Resumo, {user.nick}! 🎉',
        message='Cieszymy się, że jesteś z nami. Zacznij od stworzenia swojego pierwszego CV.',
    )


def notify_profile_complete(user):
    create_notification(
        user=user,
        type='profile',
        title='Profil w 100% ukończony! 🏆',
        message='Świetna robota! Twój profil jest kompletny.',
    )


def notify_feature(user, title, message=''):
    create_notification(
        user=user,
        type='feature',
        title=title,
        message=message,
    )
