from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',                             views.dashboard,        name='dashboard'),
    path('cv/new/',                      views.create_cv,        name='create_cv'),
    path('cv/share/<uuid:token>/',       views.share_cv,         name='share_cv'),
    path('cv/<int:cv_id>/edit/',         views.edit_cv,          name='edit_cv'),
    path('cv/<int:cv_id>/pdf/',          views.download_pdf,     name='download_pdf'),
    path('cv/<int:cv_id>/duplicate/',    views.duplicate_cv,     name='duplicate_cv'),
    path('cv/<int:cv_id>/delete/',       views.delete_cv,        name='delete_cv'),
    path('cv/<int:cv_id>/toggle-share/', views.toggle_share,     name='toggle_share'),
    path('cv/<int:cv_id>/regenerate/',   views.regenerate_token, name='regenerate_token'),
    path('cv/<int:cv_id>/stats/',        views.share_stats,      name='share_stats'),
    path('share/',                       views.share_dashboard,  name='share_dashboard'),
    path('templates/',                   views.templates,        name='templates'),
]