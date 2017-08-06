from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from ripa_archive.activity.models import Activity
from ripa_archive.documents.models import Document, DocumentData, Remark
from ripa_archive.documents.views.main import get_folder_or_404, browser_base_context
from ripa_archive.views import sendfile


def document_view(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)

    context = browser_base_context(request)
    context.update({
        "document": document,
        "parent_folder": parent_folder,
        "activities":
            Activity.objects.filter(
                content_type="documents.Document",
                target_id=document.pk
            )[:20],
        "remarks": Remark.objects.filter(edit_meta__document=document),
        "user_is_follow": request.user in document.followers.all(),
        "user_is_editor": document.current_edit_meta.editor == request.user
    })

    return TemplateResponse(template="documents_browser/single.html", request=request,
                            context=context)


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
