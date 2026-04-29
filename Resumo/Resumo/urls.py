"""
URL configuration for Resumo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name="landing_page"),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('users/', include("Users.urls")),
    path('dashboard/', include('Dashboard.urls')),
    path('notifications/', include('Notifications.urls', namespace='notifications')),
    path('ai/',        include('AI_analysis.urls',    namespace='ai_analysis')),
    path('jobs/',      include('Job_tracker.urls',     namespace='job_tracker')),
    path('linkedin/',  include('LinkedIn_import.urls', namespace='linkedin_import')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

