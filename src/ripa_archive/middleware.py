import pytz
from django.conf import settings
from django.utils import timezone
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageMiddleware(MiddlewareMixin):
    code = settings.LANGUAGE_CODE

    def process_request(self, request):
        LanguageMiddleware.code = request.session.get("language", settings.LANGUAGE_CODE)
        translation.activate(LanguageMiddleware.code)


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get('timezone')

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
