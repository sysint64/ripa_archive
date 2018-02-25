from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator, CompositeViewsAjaxFormValidator, \
    FormAjaxValidator

from ripa_archive.issues import views
from ripa_archive.issues.forms import CreateIssueForm, IssueItemForm

urlpatterns = [
    url(r'^$', views.issues, name="index"),
    url(r'^!action:create/$', views.CreateIssue.as_view(), name="create"),
    url(
        r'^!validator:create-issue/$',
        CompositeViewsAjaxFormValidator.as_view(
            views=[
                FormAjaxValidator(form=CreateIssueForm, prefix="main"),
                CompositeAjaxFormValidator(forms=[IssueItemForm]),
            ]
        ),
        name="validator-create-issue"
    )
]
