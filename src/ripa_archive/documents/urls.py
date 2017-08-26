from django.conf.urls import url

from forms.ajax import CompositeAjaxFormValidator
from ripa_archive.documents.forms.browser import *
from ripa_archive.documents.forms.single import *
from ripa_archive.documents.views import forms as forms_views
from ripa_archive.documents.views import actions as actions_views
from ripa_archive.documents.views import main as main_views
from ripa_archive.documents.views.single import forms as single_forms_views
from ripa_archive.documents.views.single import actions as single_actions_views
from ripa_archive.documents.views.single import main as single_main_view


def browser_url(regex, view, name=None, kwargs=None):
    return [
        url(r'^'+regex+'$', view, name=name, kwargs=kwargs),
        url(r'^(?P<path>[0-9a-zA-ZА-Яа-я /]+)/'+regex+'$', view, name=name, kwargs=kwargs),
    ]


def document_url(regex, view, name=None):
    if view is None:
        return []

    return browser_url(r'!document:(?P<name>[0-9a-zA-ZА-Яа-я ]+)/' + regex, view, name=name)


def folder_url(regex, view, name=None):
    return browser_url(r'!folder:(?P<name>[0-9a-zA-ZА-Яа-я ]+)/' + regex, view, name=name)


urlpatterns = \
    browser_url(r'', main_views.document_browser, name="index") + \
    browser_url(r'!archive/', main_views.document_browser, name="archive", kwargs={"archive": True}) + \
    browser_url(r'!action:create-documents/', forms_views.CreateDocuments.as_view(), name="create-documents") + \
    browser_url(r'!action:create-folders/', forms_views.CreateFolders.as_view(), name="create-folders") + \
    browser_url(r'!action:edit-permissions/', forms_views.EditFolderPermissions.as_view(), name="edit-folder-permissions") + \
    browser_url(r'!action:paste/', actions_views.paste, name="action-paste") + \
    browser_url(r'!search/', main_views.search, name="search") + \
    browser_url(r'!folder/', main_views.search, name="search")

# Form validators
urlpatterns += [
    url(r'^!validator:create-folders/$',
        CompositeAjaxFormValidator.as_view(forms=[CreateFolderForm, FolderPermissionsCreateForm]),
        name="validator-create-folders"),

    url(r'^!validator:create-documents/$',
        CompositeAjaxFormValidator.as_view(forms=[CreateDocumentForm, DocumentPermissionsCreateForm]),
        name="validator-create-documents"),

    url(r'^!validator:edit-folder-permissions/$',
        CompositeAjaxFormValidator.as_view(forms=[FolderPermissionsEditForm]),
        name="validator-edit-folder-permissions"),

    url(r'^!validator:edit-document-permissions/$',
        CompositeAjaxFormValidator.as_view(forms=[DocumentPermissionsEditForm]),
        name="validator-edit-document-permissions"),
]

# Actions
urlpatterns += [
    url(r'^!action:change-folder/$', actions_views.change_folder, name="action-change-folder"),
    url(r'^!action:delete/$', actions_views.delete, name="action-delete"),
    url(r'^!action:copy/$', actions_views.copy, name="action-copy"),
    url(r'^!action:cut/$', actions_views.cut, name="action-cut"),
    url(r'^!action:sort-by/$', actions_views.sort_by, name="sort-by"),
]

# Single document
urlpatterns += \
    document_url(r'', single_main_view.document_view, name="document") + \
    document_url(r'!file:last-version/', single_main_view.last_version_file, name="last-version-file") + \
    document_url(r'!file:(?P<version>[0-9]+)/', single_main_view.get_file, name="get-file")

# Single document forms
urlpatterns += \
    document_url(r'!action:upload-new-version/', single_forms_views.upload_new_version, name="upload-new-version") + \
    document_url(r'!action:write-remark/', single_forms_views.write_remark, name="write-remark") + \
    document_url(r'!action:rename/', single_forms_views.rename_document, name="rename-document") + \
    document_url(r'!action:edit-permissions/', forms_views.EditDocumentPermissions.as_view(), name="edit-document-permissions") + \
    document_url(r'!action:update-document-status/', single_forms_views.update_document_status, name="update-document-status")

# Single document actions
urlpatterns += \
    document_url(r'!action:take-for-revision/', single_actions_views.take_for_revision, name="take-for-revision") + \
    document_url(r'!action:toggle-follow/', single_actions_views.toggle_follow, name="follow") + \
    document_url(r'!action:revert-document/', single_actions_views.revert_document, name="revert-document") + \
    document_url(r'!action:accept-remark/', single_actions_views.accept_remark, name="accept-remark") + \
    document_url(r'!action:mark-as-finished-remark/', single_actions_views.mark_as_finished_remark, name="mark-as-finished-remark") + \
    document_url(r'!action:accept-document/', single_actions_views.accept_document, name="accept-document") + \
    document_url(r'!action:reject-document/', single_actions_views.reject_document, name="reject-document")

# Single document validators
urlpatterns += [
    url(r'^validator:upload-new-version/$',
        CompositeAjaxFormValidator.as_view(forms=[UploadNewVersionForm]),
        name="validator-upload-new-version"),

    url(r'^validator:write-remark/$',
        CompositeAjaxFormValidator.as_view(forms=[RemarkForm]),
        name="validator-write-remark"),

    url(r'^validator:rename-document/$',
        CompositeAjaxFormValidator.as_view(forms=[RenameDocumentForm]),
        name="validator-rename-document"),

    url(r'^validator:update-document-status/$',
        CompositeAjaxFormValidator.as_view(forms=[UpdateStatusForm]),
        name="validator-update-document-status"),
]

# Folder actions
urlpatterns += \
    browser_url(r'!action:rename/', single_forms_views.rename_folder, name="rename-folder")

# Folder validators
urlpatterns += [
    url(r'^validator:rename-folder/$',
        CompositeAjaxFormValidator.as_view(forms=[RenameFolderForm]),
        name="validator-rename-folder"),
]
