from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',                            views.dashboard,        name='dashboard'),
    path('cv/new/',                     views.create_cv,        name='create_cv'),
    path('cv/<int:cv_id>/edit/',        views.edit_cv,          name='edit_cv'),
    path('cv/<int:cv_id>/pdf/',         views.download_pdf,     name='download_pdf'),
    path('cv/<int:cv_id>/duplicate/',   views.duplicate_cv,     name='duplicate_cv'),
    path('cv/<int:cv_id>/delete/',      views.delete_cv,        name='delete_cv'),
]
