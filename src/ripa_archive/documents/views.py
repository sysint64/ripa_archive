from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404

from ripa_archive.documents.models import Folder


def document_browser(request, path=None):
    parent_folder = Folder.objects.get_by_path(path)
    folder = Folder()

    if parent_folder is None:
        raise Http404

    context = {
        "parent_folder": parent_folder
    }
    return render_to_response("documents_browser.html", context=context)
