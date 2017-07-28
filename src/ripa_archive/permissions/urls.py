from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive.permissions import views
from ripa_archive.permissions.forms import GroupForm
from ripa_archive.permissions.models import Group

urlpatterns = [
    url(r'^$', views.permissions, name="index"),
    url(r'^!action:create/$', views.create_group, name="action-create"),
    url(r'^!action:update/(?P<name>[0-9a-zA-ZА-Яа-я\-_ ]+)/$', views.update_group, name="action-update"),
    url(r'^!action:delete/$', views.delete_group, name="action-delete"),

    # Validators
    url(
        r'^!validator:create/$',
        CompositeAjaxFormValidator.as_view(forms=[GroupForm]),
        name="validator-create"
    ),
    url(
        r'^!validator:update/(?P<name>[0-9a-zA-ZА-Яа-я ]+)/$',
        CompositeAjaxFormValidator.as_view(
            forms=[GroupForm],
            instance_cls=Group,
            instance_query_field="name"
        ),
        name="validator-update"
    ),
]
