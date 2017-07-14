from enum import Enum

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.response import TemplateResponse
from haystack.generic_views import SearchView
from haystack.inputs import Exact
from haystack.query import SearchQuerySet

from ripa_archive.documents.models import Folder


def get_folder_or_404(path):
    folder = Folder.objects.get_by_path(path)

    if folder is None:
        raise Http404

    return folder


class SearchPlaceCode(Enum):
    THIS_FOLDER = "this-folder"
    EVERYWHERE = "everywhere"


BROWSER_SEARCH_PLACES = (
    {"name": "This folder", "code": SearchPlaceCode.THIS_FOLDER},
    {"name": "Everywhere", "code": SearchPlaceCode.EVERYWHERE},
)


@login_required(login_url="accounts:login")
def document_browser(request, path=None):
    parent_folder = get_folder_or_404(path)
    context = {
        "parent_folder": parent_folder,
        "search_places": BROWSER_SEARCH_PLACES
    }
    return TemplateResponse(template="documents_browser/list.html", request=request, context=context)


def search(request, path=None):
    place = request.GET.get("place", SearchPlaceCode.EVERYWHERE)
    query = request.GET.get("q", "")
    results = SearchQuerySet().filter(content=query)

    if place == SearchPlaceCode.THIS_FOLDER.value:
        folder = get_folder_or_404(path)
        results = SearchQuerySet().filter(content=query, parent_id=Exact(folder.id))

    context = {
        "query": query,
        "results": results,
        "search_places": BROWSER_SEARCH_PLACES
    }
    return TemplateResponse(template="search/index.html", request=request,
                            context=context)
