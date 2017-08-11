from django.db import transaction
from django.template.response import TemplateResponse

from ripa_archive.activity.models import Activity
from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions


@transaction.atomic
# @require_permissions([codes.ACTIVITY_CAN_READ])
def users_activity(request):
    context = {
        "users_activity": Activity.objects.all(),
        "active_url_name": "activity",
        "module_name": "activity",
        "title": "Users activity"
    }
    return TemplateResponse(template="activity.html", request=request, context=context)
