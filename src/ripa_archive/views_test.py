from django.http import HttpResponse


def set_ru_lang(request):
    response = HttpResponse()
    response.write("Now your language is 'Russia'")

    request.session["lang"] = "ru-RU"

    return response


def set_en_lang(request):
    response = HttpResponse()
    response.write("Now your language is 'English'")

    request.session["lang"] = "en-US"

    return response
