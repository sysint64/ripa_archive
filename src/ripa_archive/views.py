from django.shortcuts import render_to_response
from haystack.views import SearchView


def layout(request, template):
    return render_to_response("layout/{}.html".format(template))
