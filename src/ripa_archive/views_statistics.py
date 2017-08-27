from django.db import transaction
from django.template.response import TemplateResponse

from ripa_archive.accounts.models import User
from ripa_archive.activity.models import Activity
from ripa_archive.documents.models import Document


@transaction.atomic
def statistics(request):
    context = {
        "page_title": "Statistics",
        "active_url_name": "statistics",
        "total_users": User.objects.all().count(),
        "total_males": User.objects.filter(gender=User.Gender.MALE).count(),
        "total_females": User.objects.filter(gender=User.Gender.FEMALE).count(),
        "total_documents": Document.objects.all().count(),
        "total_finished_documents": Document.objects.filter(status=Document.Status.FINAL).count(),
        "total_connections": 1,
        "recent_activity": Activity.objects.all()[:10],
    }
    return TemplateResponse(template="statistics.html", request=request, context=context)
