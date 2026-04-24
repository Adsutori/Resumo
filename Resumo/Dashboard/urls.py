from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cv/new/', views.create_cv,  name='create_cv'),
    path('cv/<int:cv_id>/edit/',    views.edit_cv,    name='edit_cv'),
    path('cv/<int:cv_id>/pdf/',        views.download_pdf, name='download_pdf'),
]
