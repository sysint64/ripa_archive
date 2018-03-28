from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator, CompositeViewsAjaxFormValidator, \
    FormAjaxValidator
from ripa_archive.documents.forms.single import RemarkForm

from ripa_archive.issues.views import main as main_views
from ripa_archive.issues.views import forms as forms_views
from ripa_archive.issues.views import actions as actions_views
from ripa_archive.issues.forms import CreateIssueForm, IssueItemForm

urlpatterns = [
    url(r'^$', main_views.issues, name="index"),
    url(r'^!action:create/$', forms_views.CreateIssue.as_view(), name="create"),
    url(r'^!action:delete/$', actions_views.delete, name="delete"),

    url(r'^(?P<issue_id>[0-9]+)/$', main_views.issue, name="single"),
    url(r'^(?P<issue_id>[0-9]+)/!action:update/$', forms_views.UpdateIssue.as_view(), name="update"),
    url(r'^(?P<issue_id>[0-9]+)/(?P<issue_item_id>[0-9]+)/!action:write-remark/$', forms_views.write_remark, name="write-remark"),
    url(r'^(?P<issue_id>[0-9]+)/!action:start-working-on-item', actions_views.start_working_on_item, name="start-working-on-item"),
    url(r'^(?P<issue_id>[0-9]+)/!action:finish-working-on-item', actions_views.finish_working_on_item, name="finish-working-on-item"),
    url(r'^(?P<issue_id>[0-9]+)/!action:approve-working-on-item', actions_views.approve_working_on_item, name="approve-working-on-item"),
    url(r'^(?P<issue_id>[0-9]+)/!action:confirm-item', actions_views.confirm_item, name="confirm-item"),
    url(r'^(?P<issue_id>[0-9]+)/!action:pause-working-on-item', actions_views.pause_working_on_item, name="pause-working-on-item"),

    url(
        r'^!validator:create-issue/$',
        CompositeViewsAjaxFormValidator.as_view(
            views=[
                FormAjaxValidator(form=CreateIssueForm, prefix="main"),
                CompositeAjaxFormValidator(forms=[IssueItemForm]),
            ]
        ),
        name="validator-create-issue"
    ),

    url(
        r'^validator:write-remark/$',
        CompositeAjaxFormValidator.as_view(forms=[RemarkForm]),
        name="validator-write-remark"
    ),
]
