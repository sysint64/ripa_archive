from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive.documents.forms.browser import CreateFolderForm, CreateDocumentForm, \
    DocumentPermissionsForm, FolderPermissionsForm
from ripa_archive.documents.views import forms as forms_views
from ripa_archive.documents.views import actions as actions_views
from ripa_archive.documents.views import main
from ripa_archive.documents.views import single


def browser_url(regex, view, name=None):
    return [
        url(r'^'+regex+'$', view, name=name),
        url(r'^(?P<path>[0-9a-zA-ZА-Яа-я /]+)/'+regex+'$', view, name=name),
    ]


def document_url(regex, view, name=None):
    return browser_url(r'!document:(?P<name>[0-9a-zA-ZА-Яа-я ]+)/' + regex, view, name=name)


urlpatterns = \
    browser_url(r'', main.document_browser, name="index") + \
    browser_url(r'!action:create-documents/', forms_views.CreateDocuments.as_view(), name="create-documents") + \
    browser_url(r'!action:create-folders/', forms_views.CreateFolders.as_view(), name="create-folders") + \
    browser_url(r'!action:paste/', actions_views.paste, name="action-paste") + \
    browser_url(r'!search/', main.search, name="search")

urlpatterns += \
    document_url(r'', main.document, name="document") + \
    document_url(r'!action:take-for-revision/', single.take_for_revision, name="take-for-revision") + \
    document_url(r'!action:upload-new-version/', single.upload_new_version, name="upload-new-version") + \
    document_url(r'!action:write-remark/', single.take_for_revision, name="write-remark") + \
    document_url(r'!action:accept-remark/', single.take_for_revision, name="accept-remark") + \
    document_url(r'!action:reject-remark/', single.take_for_revision, name="reject-remark") + \
    document_url(r'!action:commit-remark/', single.take_for_revision, name="commit-remark") + \
    document_url(r'!action:accept-document/', single.take_for_revision, name="accept-document")

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
