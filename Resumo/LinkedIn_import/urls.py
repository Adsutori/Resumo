from django.urls import path
from . import views

app_name = 'linkedin_import'

urlpatterns = [
    path('', views.index, name='index'),
]