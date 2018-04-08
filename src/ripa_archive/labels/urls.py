from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive.labels import views
from ripa_archive.labels.forms import LabelForm
from ripa_archive.labels.models import Label

urlpatterns = [
    url(r'^$', views.labels, name="index"),
    url(r'^!action:create/$', views.create, name="create"),
    url(r'^(?P<label_id>[0-9]+)/!action:update/$', views.update, name="update"),

    # Validators
    url(
        r'^!validator:create/$',
        CompositeAjaxFormValidator.as_view(forms=[LabelForm]),
        name="validator-create"
    ),
    url(
        r'^(?P<id>[0-9]+)/!validator:update/$',
        CompositeAjaxFormValidator.as_view(
            forms=[LabelForm],
            instance_cls=Label,
            instance_query_field="id"
        ),
        name="validator-update"
    ),
]
