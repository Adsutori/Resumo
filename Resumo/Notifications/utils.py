import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


def create_notification(user, type, title, message='', allow_duplicates=False):
    """
    Tworzy powiadomienie dla usera.
    allow_duplicates=True → zawsze tworzy nowe (np. share, download)
    allow_duplicates=False → blokuje duplikaty tego samego typu w 24h (np. welcome, profile)
    """
    try:
        from .models import Notification
        from datetime import timedelta

        if not allow_duplicates:
            recent_cutoff = timezone.now() - timedelta(hours=24)
            already_exists = Notification.objects.filter(
                user=user,
                type=type,
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
        allow_duplicates=False,
    )


def notify_profile_complete(user):
    create_notification(
        user=user,
        type='profile',
        title='Profil w 100% ukończony! 🏆',
        message='Świetna robota! Twój profil jest kompletny.',
        allow_duplicates=False,
    )


def notify_feature(user, title, message=''):
    create_notification(
        user=user,
        type='feature',
        title=title,
        message=message,
        allow_duplicates=False,
    )
