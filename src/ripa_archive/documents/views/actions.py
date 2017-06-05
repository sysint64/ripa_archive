from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def copy(request):
    pass


@require_http_methods(["POST"])
def cut(request):
    pass


@require_http_methods(["POST"])
def paste(request):
    pass


@require_http_methods(["POST"])
def delete(request):
    pass


@require_http_methods(["POST"])
def change_folder(request):
    pass
