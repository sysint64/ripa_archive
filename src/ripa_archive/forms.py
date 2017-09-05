import pytz
from django import forms
from django.utils.translation import ugettext_lazy as _

from forms.ajax import AjaxForm


class SettingsForm(AjaxForm):
    TIMEZONES = tuple(zip(pytz.common_timezones, pytz.common_timezones))

    FORM_CHOICES = (
        ("ru", "Русский"),
        ("en", "English"),
    )

    language = forms.ChoiceField(
        label=_("Language"),
        choices=FORM_CHOICES,
        widget=forms.Select(
            attrs={
                "data-width": "fit",
            }
        )
    )
    timezone = forms.ChoiceField(
        label=_("Timezone"),
        choices=TIMEZONES,
        widget=forms.Select(
            attrs={
                "data-width": "fit",
                "data-live-search": "true"
            }
        )
    )
