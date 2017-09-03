from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        translation.activate(request.session.get("language", settings.LANGUAGE_CODE))
        print(request.session.get("language", settings.LANGUAGE_CODE))
        # lang_code = request.path.lstrip("/")[:2]
        # Language.current = Language.objects.filter(country_code=lang_code).first()
        # Language.current = Language.current or Language.objects.filter(country_code="ru").first()
        # request.language = Language.current
