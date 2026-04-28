import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


# Na górze pliku, poza klasą
DEFAULT_DESIGN = {
    'accent_color':   '#6C63FF',
    'font':           'Inter',
    'layout':         'single',   # 'single' | 'double'
    'heading_size':   'M',        # 'S' | 'M' | 'L'
    'bold_name':      True,
    'italic_summary': False,
    'show_dividers':  True,
}


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

    # --- Design (personalizacja wizualna) ---
    design = models.JSONField(default=dict, blank=True)

    # --- Udostępnianie ---
    is_shared       = models.BooleanField(default=False)
    share_token     = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    view_count      = models.PositiveIntegerField(default=0)
    share_expires   = models.DateTimeField(null=True, blank=True)

    def get_share_url(self, request=None):
        from django.urls import reverse
        path = reverse('dashboard:share_cv', kwargs={'token': str(self.share_token)})
        if request:
            return request.build_absolute_uri(path)
        return path

    def is_share_active(self):
        if not self.is_shared:
            return False
        if self.share_expires and self.share_expires < timezone.now():
            return False
        return True


    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'CV'
        verbose_name_plural = 'CV'

    def __str__(self):
        return f"{self.title} ({self.user.username})"

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


class CVView(models.Model):
    """Pojedyncze wyświetlenie udostępnionego CV."""
    cv         = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='views')
    viewed_at  = models.DateTimeField(auto_now_add=True)
    ip_hash    = models.CharField(max_length=64, blank=True)  # zahashowane IP

    class Meta:
        ordering = ['-viewed_at']