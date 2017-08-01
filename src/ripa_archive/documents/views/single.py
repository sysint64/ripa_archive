from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ripa_archive.documents.forms.single import UploadNewVersionForm
from ripa_archive.documents.models import Document, DocumentEditMeta, DocumentData
from ripa_archive.documents.views.main import get_folder_or_404, browser_base_context
from ripa_archive.permissions.decorators import require_permissions
from ripa_archive.views import sendfile


def get_document(*args, **kwargs):
    path, name = kwargs.get("path"), kwargs["name"]
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)
    return document


@api_view(["POST"])
@require_permissions(["documents_can_take_for_revision"], get_instance_functor=get_document)
def take_for_revision(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.is_under_edition:
        raise ValidationError("Already under edition")

    # Attach editor to document
    DocumentEditMeta.objects.create(editor=request.user, document=document)
    messages.success(request, "Successfully took")

    return Response({}, status=status.HTTP_200_OK)


@require_http_methods(["GET"])
def last_version_file(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)

    return sendfile(request, str(document.data.file.file), force_download=True)


@require_http_methods(["GET"])
def get_file(request, name, version, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)
    data = get_object_or_404(DocumentData, document=document, pk=version)

    return sendfile(request, str(data.file.file), force_download=True)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def upload_new_version(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)

    if request.method == "POST":
        # No instance because need new version of document and save old version
        form = UploadNewVersionForm(request.POST, request.FILES)
    else:
        form = UploadNewVersionForm(instance=document.data)

    context = browser_base_context(request)
    context.update({
        "form_title": "Upload new version",
        "form": form,
        "submit_title": "Upload",
        "validator_url": reverse("documents:validator-upload-new-version"),
    })

    if request.method == "POST" and form.is_valid():
        data = form.save(commit=False)
        data.document = document
        data.save()

        document.data = data
        document.current_edit_meta.end_datetime = timezone.now()
        document.current_edit_meta.closed = True
        document.current_edit_meta.save()
        document.save()

        messages.success(request, "Successfully uploaded")
        return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)
