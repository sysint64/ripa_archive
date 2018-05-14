from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm

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
        fields = "parent", \
                 "email", "first_name", "last_name", "gender", "location", "position", "web_site", \
                 "group", "is_active", \
                 "avatar_image"

    parent = forms.ModelChoiceField(
        label=_("Parent"),
        required=False,
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            "data-width": "fit",
        }),
    )

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


class UserUpdatePasswordForm(AjaxForm):
    def __init__(self, data=None, files=None, instance=None):
        self.instance = instance
        super().__init__(data=data, files=files)

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")

        if not self.instance.check_password(old_password):
            raise forms.ValidationError(
                "Неверный пароль",
                code='password_mismatch',
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                UserCreationForm.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        # password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2
