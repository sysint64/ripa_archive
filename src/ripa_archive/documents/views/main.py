from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.urls import reverse

from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm
from ripa_archive.documents.models import Folder, DocumentType


def get_folder_or_404(path):
    folder = Folder.objects.get_by_path(path)

    if folder is None:
        raise Http404

    return folder


def document_browser(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder
    }
    return render_to_response("documents_browser/list.html", context=context)


def edit(request):
    pass


def create_folders(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder,
        "form_title": "Create folders",
        "form": CreateFolderForm(),
        "validator-url": reverse("documents:validator-create-folder")
    }
    return render_to_response("documents_browser/multi-form.html", context=context)


def create_documents(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder,
        "form_title": "Create documents",
        "form": CreateDocumentForm(),
        "validator-url": reverse("documents:validator-create-document")
    }
    return render_to_response("documents_browser/multi-form.html", context=context)
