from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse

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


def document_browser(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder,
        "search_places": BROWSER_SEARCH_PLACES
    }
    return render_to_response("documents_browser/list.html", context=context)


def edit(request):
    pass


def create_folders(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder,
        "form_title": "Create folders",
        "validator_url": reverse("documents:validator-create-folder"),
        "search_places": BROWSER_SEARCH_PLACES,
        "form": CreateFolderForm(),
        # "permissions_form": PermissionsForm(),
    }
    context.update(csrf(request))
    return render_to_response("forms/multi-form.html", context=context)


def create_documents(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder,
        "form_title": "Create documents",
        "form": CreateDocumentForm(),
        "validator_url": reverse("documents:validator-create-document"),
        "search_places": BROWSER_SEARCH_PLACES,
    }
    context.update(csrf(request))
    return render_to_response("forms/multi-form.html", context=context)
