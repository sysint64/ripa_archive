from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive.permissions import views
from ripa_archive.permissions.forms import CreateGroupForm
from ripa_archive.permissions.models import Group

urlpatterns = [
    url(r'^$', views.permissions, name="index"),
    url(r'^!action:create-group/$', views.create_group, name="create-group"),
    url(r'^!action:update-group/(?P<name>[0-9a-zA-ZА-Яа-я ]+)/$', views.update_group, name="update-group"),

    url(
        r'^!validator:create-group/$',
        CompositeAjaxFormValidator.as_view(forms=[CreateGroupForm]),
        name="validator-create-group"
    ),
    url(
        r'^!validator:update-group/(?P<name>[0-9a-zA-ZА-Яа-я ]+)/$',
        CompositeAjaxFormValidator.as_view(
            forms=[CreateGroupForm],
            instance_cls=Group,
            instance_query_field="name"
        ),
        name="validator-update-group"
    ),
]
