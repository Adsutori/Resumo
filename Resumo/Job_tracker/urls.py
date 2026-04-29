from django.urls import path
from . import views

app_name = 'job_tracker'

urlpatterns = [
    path('', views.index, name='index'),
]