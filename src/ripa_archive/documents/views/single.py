from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ripa_archive.documents.forms.single import TakeForRevisionForm
from ripa_archive.documents.models import Document
from ripa_archive.documents.views.main import get_folder_or_404, browser_base_context


@api_view(["POST"])
def take_for_revision(request, name, path=None):
    return Response({}, status=status.HTTP_200_OK)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def upload_new_version(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)

    form = TakeForRevisionForm(request.POST)

    context = browser_base_context(request)
    context.update({
        "form_title": "Take for revision",
        "form": form,
        "submit_title": "Take",
        # "validator_url": reverse("permissions:validator-create"),
    })

    return TemplateResponse(template="forms/form.html", request=request, context=context)
