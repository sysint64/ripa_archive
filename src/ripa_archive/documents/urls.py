from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm, \
    DocumentPermissionsForm, FolderPermissionsForm
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
    browser_url(r'!document:(?P<name>[0-9a-zA-ZА-Яа-я ]+)', main.document, name="document") + \
    browser_url(r'!action:create-documents/', forms_views.CreateDocuments.as_view(), name="create-documents") + \
    browser_url(r'!action:create-folders/', forms_views.CreateFolders.as_view(), name="create-folders") + \
    browser_url(r'!action:paste/', actions_views.paste, name="action-paste") + \
    browser_url(r'!search/', main.search, name="search")

# Actions
urlpatterns += [
    url(r'^!action:change-folder/$', actions_views.change_folder, name="action-change-folder"),
    url(r'^!action:delete/$', actions_views.delete, name="action-delete"),
    url(r'^!action:copy/$', actions_views.copy, name="action-copy"),
    url(r'^!action:cut/$', actions_views.cut, name="action-cut"),
]

# Form validators
urlpatterns += [
    url(r'^!validator:create-folders/$',
        CompositeAjaxFormValidator.as_view(forms=[CreateFolderForm, FolderPermissionsForm]),
        name="validator-create-folders"),

    url(r'^!validator:create-documents/$',
        CompositeAjaxFormValidator.as_view(forms=[CreateDocumentForm, DocumentPermissionsForm]),
        name="validator-create-documents"),
]
