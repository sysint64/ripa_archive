from django.shortcuts import render_to_response


def layout(request, template):
    return render_to_response("layout/{}.html".format(template))
