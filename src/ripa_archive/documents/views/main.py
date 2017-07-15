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

    @staticmethod
    def get_from_code(code):
        for item in SearchPlaceCode:
            print(item)
            if item.value == code:
                return item

    def get_name(self):
        for place in BROWSER_SEARCH_PLACES:
            if self.value == place["code"]:
                return place["name"]

        return self.value


BROWSER_SEARCH_PLACES = (
    {"name": "This folder", "code": SearchPlaceCode.THIS_FOLDER.value},
    {"name": "Everywhere", "code": SearchPlaceCode.EVERYWHERE.value},
)


@login_required(login_url="accounts:login")
def document_browser(request, path=None):
    parent_folder = get_folder_or_404(path)
    parent_folder_url = ""

    if parent_folder.parent is not None:
        parent_folder_url = parent_folder.parent.permalink

    context = {
        "parent_folder": parent_folder,
        "parent_folder_url": parent_folder_url,
        "search_places": BROWSER_SEARCH_PLACES
    }
    return TemplateResponse(template="documents_browser/list.html", request=request, context=context)


def search(request, path=None):
    place = request.GET.get("place", SearchPlaceCode.EVERYWHERE)
    query = request.GET.get("q", "")
    results = SearchQuerySet().filter(content=query)

    suggestion = results.spelling_suggestion()
    print("suggestions")
    print(suggestion)

    if place == SearchPlaceCode.THIS_FOLDER.value:
        folder = get_folder_or_404(path)
        results = SearchQuerySet().filter(content=query, parent_id=Exact(folder.id))

    context = {
        "back_url": request.path.split("!")[0],
        "query": query,
        "results": results,
        "search_places": BROWSER_SEARCH_PLACES
    }
    return TemplateResponse(template="search/index.html", request=request,
                            context=context)
