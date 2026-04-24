from django.contrib import admin
from .models import CV


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'template', 'progress', 'is_active', 'is_shared', 'updated_at')
    list_filter   = ('template', 'is_active', 'is_shared')
    search_fields = ('title', 'user__username', 'user__email')
    readonly_fields = ('share_token', 'download_count', 'view_count', 'created_at', 'updated_at')
