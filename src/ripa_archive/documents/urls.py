from django.conf.urls import url

from forms.ajax import FormAjaxValidator
from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm
from ripa_archive.documents.views import forms as forms_views
from ripa_archive.documents.views import actions as actions_views
from ripa_archive.documents.views import main


def browser_url(regex, view, name=None):
    return [
        url(r'^'+regex+'$', view, name=name),
        url(r'^(?P<path>[0-9a-zA-ZА-Яа-я /]+)/'+regex+'$', view, name=name),
    ]

urlpatterns = \
    browser_url(r'', main.document_browser, name="browser") + \
    browser_url(r'!action:create-documents/', forms_views.CreateDocuments.as_view(), name="create-documents") + \
    browser_url(r'!action:create-folders/', forms_views.CreateFolders.as_view(), name="create-folders")

# Actions
urlpatterns += [
    url(r'^!action:change-folder/$', actions_views.change_folder, name="action-change-folder")
]

# Form validators
urlpatterns += [
    url(r'^!validator:create-folders/$', FormAjaxValidator.as_view(form=CreateFolderForm),
        name="validator-create-folders"),
    url(r'^!validator:create-documents/$', FormAjaxValidator.as_view(form=CreateDocumentForm),
        name="validator-create-documents"),
]
