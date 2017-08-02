from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive.documents.forms.browser import CreateFolderForm, CreateDocumentForm, \
    DocumentPermissionsForm, FolderPermissionsForm
from ripa_archive.documents.forms.single import UploadNewVersionForm, RenameFolder, RenameDocument
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

def folder_url(regex, view, name=None):
    return browser_url(r'!folder:(?P<name>[0-9a-zA-ZА-Яа-я ]+)/' + regex, view, name=name)


urlpatterns = \
    browser_url(r'', main.document_browser, name="index") + \
    browser_url(r'!action:create-documents/', forms_views.CreateDocuments.as_view(), name="create-documents") + \
    browser_url(r'!action:create-folders/', forms_views.CreateFolders.as_view(), name="create-folders") + \
    browser_url(r'!action:paste/', actions_views.paste, name="action-paste") + \
    browser_url(r'!search/', main.search, name="search") + \
    browser_url(r'!folder/', main.search, name="search")

urlpatterns += \
    document_url(r'', main.document, name="document") + \
    document_url(r'!file:last-version/', single.last_version_file, name="last-version-file") + \
    document_url(r'!file:(?P<version>[0-9]+)/', single.get_file, name="get-file") + \
    document_url(r'!action:take-for-revision/', single.take_for_revision, name="take-for-revision") + \
    document_url(r'!action:upload-new-version/', single.upload_new_version, name="upload-new-version") + \
    document_url(r'!action:write-remark/', single.take_for_revision, name="write-remark") + \
    document_url(r'!action:accept-remark/', single.take_for_revision, name="accept-remark") + \
    document_url(r'!action:reject-remark/', single.take_for_revision, name="reject-remark") + \
    document_url(r'!action:commit-remark/', single.take_for_revision, name="commit-remark") + \
    document_url(r'!action:accept-document/', single.take_for_revision, name="accept-document") + \
    document_url(r'!action:rename/', single.rename_document, name="rename-document")

urlpatterns += \
    folder_url(r'!action:rename/', single.rename_folder, name="rename-folder")

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

    url(r'^validator:upload-new-version/$',
        CompositeAjaxFormValidator.as_view(forms=[UploadNewVersionForm]),
        name="validator-upload-new-version"),

    url(r'^validator:rename-folder/$',
        CompositeAjaxFormValidator.as_view(forms=[RenameFolder]),
        name="validator-rename-folder"),

    url(r'^validator:rename-document/$',
        CompositeAjaxFormValidator.as_view(forms=[RenameDocument]),
        name="validator-rename-document"),
]
