from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.context_processors import csrf
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View

from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm, PermissionsForm
from ripa_archive.documents.models import Folder, DocumentType


def get_folder_or_404(path):
    folder = Folder.objects.get_by_path(path)

    if folder is None:
        raise Http404

    return folder


BROWSER_SEARCH_PLACES = (
    {"name": "This folder", "code": "this-folder"},
    {"name": "Everywhere", "code": "everywhere"},
)


@login_required(login_url="accounts:login")
def document_browser(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder,
        "search_places": BROWSER_SEARCH_PLACES
    }
    return TemplateResponse(template="documents_browser/list.html", request=request, context=context)
