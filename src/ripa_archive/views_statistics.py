from datetime import timedelta, datetime, date
from django.db import transaction
from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone

from ripa_archive.accounts.models import User
from ripa_archive.activity.models import Activity
from ripa_archive.documents.models import Document, DocumentEditMeta
from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions


@transaction.atomic
@require_permissions([codes.STATISTICS_CAN_READ])
def statistics(request):
    accepted_documents = Document.objects.filter(
        ~Q(accepted_edit_meta=None) &
        Q(accepted_edit_meta__status=DocumentEditMeta.Status.ACCEPTED)
    ).order_by("-accepted_edit_meta__end_datetime")

    rejected_documents = Document.objects.filter(
        ~Q(accepted_edit_meta=None) &
        Q(accepted_edit_meta__status=DocumentEditMeta.Status.REJECTED)
    ).order_by("-accepted_edit_meta__end_datetime")

    took_for_revision_documents = Document.objects.filter(
        ~Q(current_edit_meta=None) &
        Q(current_edit_meta__status=DocumentEditMeta.Status.ACTIVE)
    ).order_by("-accepted_edit_meta__end_datetime")

    default_start_date = timezone.now() - timedelta(days=30)
    start_date = request.GET.get("start_date", default_start_date.strftime("%Y-%m-%d"))
    end_date = request.GET.get("end_date", timezone.now().strftime("%Y-%m-%d"))
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    accepted_points = {}
    rejected_points = {}

    def get_plot_points(qs, points):
        filtered_qs = qs.filter(
            accepted_edit_meta__start_datetime__gte=start_date,
            accepted_edit_meta__start_datetime__lte=end_date + timedelta(days=1)
        )
        total = 0

        for document in filtered_qs:
            key = document.accepted_edit_meta.end_datetime.strftime("%Y-%m-%d")
            total += 1

            # Fill gaps
            if key not in accepted_points:
                accepted_points[key] = 0

            if key not in rejected_points:
                rejected_points[key] = 0

            points[key] = points[key] + 1 if key in points else 1

        return total

    total_accepted = get_plot_points(accepted_documents, accepted_points)
    total_rejected = get_plot_points(rejected_documents, rejected_points)

    total = total_accepted + total_rejected

    if total == 0:
        accepted_documents_percent = 0
        rejected_documents_percent = 0
    else:
        accepted_documents_percent = round(total_accepted / total * 100)
        rejected_documents_percent = round(total_rejected / total * 100)

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
        "last_edited_documents": accepted_documents[:5],
        "last_took_for_revision_documents": took_for_revision_documents[:5],
        "accepted_documents_percent": accepted_documents_percent,
        "rejected_documents_percent": rejected_documents_percent,
        "accepted_points": accepted_points,
        "rejected_points": rejected_points
    }
    return TemplateResponse(template="statistics.html", request=request, context=context)
