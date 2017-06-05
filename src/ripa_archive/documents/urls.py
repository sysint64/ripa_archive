from django.conf.urls import url

from forms.ajax import FormAjaxValidation
from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm
from ripa_archive.documents.views import main


def browser_url(regex, view, name=None):
    return [
        url(r'^'+regex+'$', view, name=name),
        url(r'^(?P<path>[0-9a-zA-Z /]+)/'+regex+'$', view, name=name),
    ]

urlpatterns = \
    browser_url(r'', main.document_browser, name="browser") + \
    browser_url(r'!action:create-documents/', main.create_documents, name="create-documents") + \
    browser_url(r'!action:create-folders/', main.create_folders, name="create-folders")

# Form validators
urlpatterns += [
    url(r'^!validator:create-folder/$', FormAjaxValidation.as_view(form=CreateFolderForm),
        name="validator-create-folder"),
    url(r'^!validator:create-document/$', FormAjaxValidation.as_view(form=CreateDocumentForm),
        name="validator-create-document"),
]
