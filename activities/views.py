from django.shortcuts import render

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from .models import Notification
from .decorators import ajax_required

@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()        
    return render(request, 'activities/notifications.html', {'notifications': notifications})

@login_required
@ajax_required
def last_notifications(request):
    import time
    time.sleep(2)
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'activities/last_notifications.html', {'notifications': notifications})

@login_required
@ajax_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    return HttpResponse(len(notifications))