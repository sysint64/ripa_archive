from django import forms
from django.contrib.auth import authenticate

from forms.ajax import AjaxForm


class LoginForm(AjaxForm):
    email = forms.EmailField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "Номер телефона или E-mail"}
        ),
    )
    password = forms.CharField(
        strip=False,
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Не менее 4 символов"}
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
                "invalid email or password",
                code='invalid_login',
                params={'username': "email"},
            )
