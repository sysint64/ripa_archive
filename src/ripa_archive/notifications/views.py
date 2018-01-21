from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.template.response import TemplateResponse

from ripa_archive.notifications.models import Notification


@login_required(login_url="accounts:login")
def notifications(request):
    notifications = []

    with transaction.atomic():
        for notification in Notification.objects.filter(to=request.user):
            notifications.append(notification)

        Notification.objects.filter(to=request.user).update(is_read=True)

    context = {
        "notifications": notifications
    }

    return TemplateResponse(template="notifications.html", request=request, context=context)
