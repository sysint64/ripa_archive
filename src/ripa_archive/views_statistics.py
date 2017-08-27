from django.db import transaction
from django.db.models import Q
from django.template.response import TemplateResponse

from ripa_archive.accounts.models import User
from ripa_archive.activity.models import Activity
from ripa_archive.documents.models import Document, DocumentEditMeta


@transaction.atomic
def statistics(request):
    last_edited_documents = Document.objects.filter(
        ~Q(accepted_edit_meta=None) &
        Q(accepted_edit_meta__status=DocumentEditMeta.Status.ACCEPTED)
    ).order_by("-accepted_edit_meta__end_datetime")[:5]

    last_took_for_revision_documents = Document.objects.filter(
        ~Q(current_edit_meta=None) &
        Q(current_edit_meta__status=DocumentEditMeta.Status.ACTIVE)
    ).order_by("-accepted_edit_meta__end_datetime")[:5]

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
        "last_edited_documents": last_edited_documents,
        "last_took_for_revision_documents": last_took_for_revision_documents,
    }
    return TemplateResponse(template="statistics.html", request=request, context=context)
