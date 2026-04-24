import uuid
from django.db import models
from django.conf import settings


class CV(models.Model):

    TEMPLATE_CHOICES = [
        ('classic', 'Classic'),
        ('modern',  'Modern'),
        ('minimal', 'Minimal'),
    ]

    # --- Relacja ---
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cvs'
    )

    # --- Podstawowe dane ---
    title    = models.CharField(max_length=200)
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='classic')
    content  = models.JSONField(default=dict)   # wszystkie dane CV (sekcje)
    progress = models.IntegerField(default=0)   # % wypełnienia (0–100)

    # --- Statusy ---
    is_active = models.BooleanField(default=True)

    # --- Udostępnianie ---
    share_token    = models.UUIDField(default=uuid.uuid4, unique=True)
    is_shared      = models.BooleanField(default=False)

    # --- Statystyki ---
    download_count = models.IntegerField(default=0)
    view_count     = models.IntegerField(default=0)

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'CV'
        verbose_name_plural = 'CV'

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    def get_share_url(self):
        return f"/cv/share/{self.share_token}/"

    def calculate_progress(self):
        """Oblicza % wypełnienia na podstawie sekcji w content."""
        sections = [
            'personal',
            'summary',
            'experience',
            'education',
            'skills',
            'languages',
            'links',
        ]
        if not self.content:
            return 0

        filled = sum(1 for s in sections if self.content.get(s))
        progress = int((filled / len(sections)) * 100)
        self.progress = progress
        self.save(update_fields=['progress'])
        return progress
