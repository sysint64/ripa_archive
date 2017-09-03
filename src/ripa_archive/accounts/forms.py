from django import forms
from django.contrib.auth import authenticate

from forms.ajax import AjaxForm, AjaxModelForm
from forms.consts import YES_NO_CHOICES
from ripa_archive.accounts.models import User
from ripa_archive.permissions.models import Group
from django.utils.translation import ugettext_lazy as _


class LoginForm(AjaxForm):
    email = forms.EmailField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": _("E-mail")}
        ),
    )
    password = forms.CharField(
        strip=False,
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": _("At least 4 characters")}
        )
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email or not password:
            return self.cleaned_data

        self.user = authenticate(email=email, password=password)

        if self.user is None:
            raise forms.ValidationError(
                _("invalid email or password"),
                code='invalid_login',
                params={'username': "email"},
            )


class UserForm(AjaxModelForm):
    class Meta:
        model = User
        fields = "email", "first_name", "last_name", "gender", "location", "position", "web_site", \
                 "group", "is_active", \
                 "avatar_image"

    gender = forms.ChoiceField(
        label=_("Gender"),
        required=False,
        choices=User.Gender.CHOICES,
        widget=forms.Select(attrs={
            "data-width": "fit",
        }),
    )

    group = forms.ModelChoiceField(
        label=_("Group"),
        required=False,
        empty_label=None,
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={
            "data-width": "fit",
        }),
    )

    is_active = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        label=_("Is active"),
        widget=forms.Select(attrs={
            "data-width": "fit",
        }),
    )
