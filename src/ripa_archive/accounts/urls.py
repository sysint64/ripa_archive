from django.conf.urls import url
from django.contrib.auth.views import logout

from forms.ajax import FormAjaxValidator
from ripa_archive.accounts import views
from ripa_archive.accounts.forms import LoginForm

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', logout, {'next_page': '/accounts/login/'}, name="logout"),
    url(r'^!validator:login-validator/$', FormAjaxValidator.as_view(form=LoginForm), name="login-validator"),

    # Users
    url(r'^$', views.users, name="index"),
    # url(r'^!action:create-group/$', views.create_group, name="create-group"),
    # url(r'^!action:update-group/(?P<name>[0-9a-zA-ZА-Яа-я ]+)/$', views.update_group, name="update-group"),
]
