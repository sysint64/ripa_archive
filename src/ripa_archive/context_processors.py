from django.conf import settings

from ripa_archive.documents.views.main import SearchPlaceCode
from ripa_archive.notifications.models import Notification


def search(request):
    search_place = SearchPlaceCode.get_from_code(request.GET.get("place"))

    if search_place is None:
        search_place = SearchPlaceCode.THIS_FOLDER

    is_documents = request.path.split("/")[1] == "documents"

    if not is_documents:
        search_url = "/documents/!search/"
    else:
        search_url = request.path.split("!")[0] + "!search/"

    return {
        "search_url": search_url,
        "search_place": search_place.value,
        "search_place_name": search_place.get_name()
    }


def common(request):
    # exclamation_split = request.path.split("!")

    context = {
        # "up_action_url": "!".join(x for i, x in enumerate(exclamation_split) if i < len(exclamation_split) - 1),
        "up_action_url": request.path.split("!")[0],
        "up_url": request.path.split("/")[0],
    }

    if not request.user.is_anonymous:
        context.update({
            "have_notifications": Notification.objects.filter(to=request.user, is_read=False).count() > 0,
            "project_title": settings.PROJECT_TITLE,
            "project_version": settings.PROJECT_VERSION,
            "language_code": request.session.get("language", settings.LANGUAGE_CODE)
        })

    return context
