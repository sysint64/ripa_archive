from django.http import HttpResponse


def set_ru_lang(request):
    response = HttpResponse()
    response.write("Now your language is 'Russia'")

    request.session["language"] = "ru"

    return response


def set_en_lang(request):
    response = HttpResponse()
    response.write("Now your language is 'English'")

    request.session["language"] = "en"

    return response
