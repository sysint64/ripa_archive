from enum import Enum

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from haystack.inputs import Exact
from haystack.query import SearchQuerySet

from ripa_archive.documents.models import Folder, Document
from ripa_archive.permissions import codes


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
    {"name": _("This folder"), "code": SearchPlaceCode.THIS_FOLDER.value},
    {"name": _("Everywhere"), "code": SearchPlaceCode.EVERYWHERE.value},
)

BROWSER_ADD_MENU = (
    {"name": _("Folder(s)"), "permalink": "!action:create-folders"},
    {"name": _("Document(s)"), "permalink": "!action:create-documents"},
)


def browser_base_context(request):
    return {
        "active_url_name": "documents",
        "search_places": BROWSER_SEARCH_PLACES,
        "add_menu": BROWSER_ADD_MENU
    }


@login_required(login_url="accounts:login")
def document_browser(request, path=None, archive=False):
    parent_folder = get_folder_or_404(path)
    parent_folder_url = ""

    if not parent_folder.is_user_has_permission(request.user, codes.FOLDERS_CAN_READ):
        raise PermissionDenied()

    if parent_folder.parent is not None:
        parent_folder_url = parent_folder.parent.permalink

    sort_by, sort_direction = request.session.get("documents-sort-by", "name,asc").split(",")

    def apply_sort(queryset):
        if queryset.model == Folder and sort_by != "name":
            return queryset

        qs_sort_direction = {
            "asc": "",
            "desc": "-",
        }.get(sort_direction)

        qs_sort_field = {
            "datetime": "data__datetime"
        }.get(sort_by, sort_by)

        return queryset.order_by("%s%s" % (qs_sort_direction, qs_sort_field))

    sorting_css_classes = {"name": "", "status": "", "datetime": "", sort_by: sort_direction}

    folders = apply_sort(Folder.objects.for_user(request.user, parent_folder))
    documents = apply_sort(Document.objects.for_user(request.user, parent_folder))

    context = browser_base_context(request)
    context.update({
        "sorting_name_css_classes": sorting_css_classes["name"],
        "sorting_status_css_classes": sorting_css_classes["status"],
        "sorting_datetime_css_classes": sorting_css_classes["datetime"],
        "parent_folder": parent_folder,
        "parent_folder_url": parent_folder_url,
        "folders": folders,
        "documents": documents,
    })

    if archive:
        context.update({
            "active_url_name": "archive",
            "documents": documents.filter(status=Document.Status.FINAL),
            "archive": True,
        })
    else:
        context.update({
            "documents": documents.filter(~Q(status=Document.Status.FINAL)),
        })

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
        results = SearchQuerySet().filter(content=query, parent_ids=Exact(folder.pk))

    context = browser_base_context(request)
    context.update({
        "back_url": request.path.split("!")[0],
        "query": query,
        "results": results,
    })
    return TemplateResponse(template="search/index.html", request=request,
                            context=context)
