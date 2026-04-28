# notifications/views.py

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:30]

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).count()

    data = [
        {
            'id':         n.id,
            'type':       n.type,
            'icon':       n.icon,
            'title':      n.title,
            'message':    n.message,
            'is_read':    n.is_read,
            'created_at': n.created_at.strftime('%d.%m.%Y %H:%M'),
        }
        for n in notifications
    ]

    return JsonResponse({
        'notifications': data,
        'unread_count':  unread_count,
    })


@login_required
@require_POST
def mark_all_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def mark_read(request, notification_id):
    Notification.objects.filter(
        pk=notification_id,
        user=request.user,
    ).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def delete_notification(request, notification_id):
    Notification.objects.filter(
        pk=notification_id,
        user=request.user,
    ).delete()
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def delete_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'ok'})
