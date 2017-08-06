from django.http import Http404


def get_request_int_or_404(request, data_dict, name):
    data = getattr(request, data_dict)
    item_id = data.get(name)

    try:
        item_id = int(item_id)
    except ValueError:
        raise Http404()

    return item_id
