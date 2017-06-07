from django.conf.urls import url

from forms.ajax import FormAjaxValidator
from ripa_archive.accounts import views
from ripa_archive.accounts.forms import LoginForm

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^login-validator/$', FormAjaxValidator.as_view(form=LoginForm), name="login-validator"),
]
