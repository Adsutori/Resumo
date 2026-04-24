from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Usuwa niezweryfikowane konta starsze niż 15 minut'

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(minutes=15)

        expired_users = User.objects.filter(
            is_active=False,
            is_verified=False,
            created_at__lt=cutoff
        )

        count = expired_users.count()
        expired_users.delete()

        self.stdout.write(
            self.style.SUCCESS(f'Usunięto {count} niezweryfikowanych kont.')
        )
