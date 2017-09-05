from django.conf import settings
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ripa_archive.forms import SettingsForm
from ripa_archive.middleware import LanguageMiddleware


def settings_view(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
    else:
        form = SettingsForm(
            initial={
                "language": LanguageMiddleware.code,
                "timezone": request.session.get('timezone', settings.TIME_ZONE)
            }
        )

    context = {
        "form_title": _("Settings"),
        "form": form,
        "submit_title": _("Save"),
        "validator_url": reverse("validator-settings"),
    }

    if request.method == "POST" and form.is_valid():
        request.session["language"] = form.cleaned_data["language"]
        request.session["timezone"] = form.cleaned_data["timezone"]
        return redirect("settings")

    return TemplateResponse(template="forms/form.html", request=request, context=context)
