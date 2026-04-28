from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('list/',                          views.notifications_list,     name='list'),
    path('mark-all-read/',                 views.mark_all_read,          name='mark_all_read'),
    path('<int:notification_id>/read/',    views.mark_read,              name='mark_read'),
    path('<int:notification_id>/delete/',  views.delete_notification,    name='delete'),
    path('delete-all/',                    views.delete_all_notifications, name='delete_all'),
]
