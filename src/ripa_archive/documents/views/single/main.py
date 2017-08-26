from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from ripa_archive.activity.models import Activity
from ripa_archive.documents.models import Document, DocumentData, Remark, Folder
from ripa_archive.documents.views.main import get_folder_or_404, browser_base_context
from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions
from ripa_archive.views import sendfile


def get_document(*args, **kwargs):
    path, name = kwargs.get("path"), kwargs["name"]
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, name=name)
    return document


def get_folder(*args, **kwargs):
    return get_folder_or_404(kwargs.get("path"))


@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_READ], get_instance_functor=get_document)
def document_view(request, name, path=None):
    document = get_document(name=name, path=path)

    context = browser_base_context(request)
    context.update({
        "document": document,
        "users_activity":
            Activity.objects.filter(
                content_type="documents.Document",
                target_id=document.pk
            )[:20],
        "remarks": Remark.active_objects.filter(edit_meta__document=document),
        "user_is_follow": request.user in document.followers.all(),
        "user_is_editor": document.current_edit_meta is not None and document.current_edit_meta.editor == request.user,
        "archive": document.status == Document.Status.FINAL
    })

    if document.status == Document.Status.FINAL:
        context.update({
            "active_url_name": "archive",
        })

    return TemplateResponse(template="documents_browser/single/index.html", request=request,
                            context=context)


@require_http_methods(["GET"])
@require_permissions([codes.DOCUMENTS_CAN_READ_LAST_VERSION], get_instance_functor=get_document)
def last_version_file(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, name=name)

    return sendfile(request, str(document.data.file.file), force_download=True)


@require_http_methods(["GET"])
@require_permissions([codes.DOCUMENTS_CAN_READ_PREVIOUS_VERSIONS], get_instance_functor=get_document)
def get_file(request, name, version, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, name=name)
    data = get_object_or_404(DocumentData, document=document, pk=version)

    return sendfile(request, str(data.file.file), force_download=True)
