from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.response import TemplateResponse

from ripa_archive.notifications.models import Notification


@login_required(login_url="accounts:login")
def notifications(request):
    context = {
        "notifications": Notification.objects.filter(to=request.user)
    }

    return TemplateResponse(template="notifications.html", request=request,
                            context=context)
