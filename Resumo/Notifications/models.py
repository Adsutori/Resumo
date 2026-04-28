from django.db import models
from django.conf import settings


class Notification(models.Model):

    TYPE_CHOICES = [
        ('welcome',         'Pierwsze logowanie'),
        ('profile',         'Ukończenie profilu'),
        ('feature',         'Nowa funkcja'),
        ('share',           'Udostępnienie CV'),
        ('download',        'Pobranie PDF'),
        ('info',            'Informacja'),
    ]

    ICON_MAP = {
        'welcome':  'party-popper',
        'profile':  'user-check',
        'feature':  'sparkles',
        'share':    'share-2',
        'download': 'download',
        'info':     'info',
    }

    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type       = models.CharField(max_length=30, choices=TYPE_CHOICES, default='info')
    title      = models.CharField(max_length=200)
    message    = models.TextField(blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Powiadomienie'
        verbose_name_plural = 'Powiadomienia'

    def __str__(self):
        return f'[{self.type}] {self.title} → {self.user.nick}'

    @property
    def icon(self):
        return self.ICON_MAP.get(self.type, 'bell')
