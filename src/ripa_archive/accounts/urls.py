from django.conf.urls import url
from django.contrib.auth.views import logout

from forms.ajax import FormAjaxValidator, CompositeAjaxFormValidator
from ripa_archive.accounts import views
from ripa_archive.accounts.forms import LoginForm, UserForm
from ripa_archive.accounts.models import User

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', logout, {'next_page': '/accounts/login/'}, name="logout"),
    url(r'^!validator:login-validator/$', CompositeAjaxFormValidator.as_view(forms=[LoginForm]), name="login-validator"),

    # Users
    url(r'^$', views.users, name="index"),
    url(r'^(?P<user_id>[0-9]+)/$', views.profile, name="profile"),
    url(r'^(?P<user_id>[0-9]+)/!action:update/$', views.update, name="update"),
    url(r'^!action:create/$', views.create, name="create"),
    # url(r'^!action:update/(?P<email>[0-9a-zA-ZА-Яа-я.\-_@]+)/$', views.update, name="update"),
    url(r'^!action:delete/$', views.delete, name="delete"),

    # Validators
    url(
        r'^!validator:create/$',
        CompositeAjaxFormValidator.as_view(forms=[UserForm]),
        name="validator-create"
    ),
    url(
        r'^(?P<id>[0-9]+)/!validator:update/$',
        CompositeAjaxFormValidator.as_view(
            forms=[UserForm],
            instance_cls=User,
            instance_query_field="id"
        ),
        name="validator-update"
    ),
]
