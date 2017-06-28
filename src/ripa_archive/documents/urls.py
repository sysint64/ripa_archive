from django.conf.urls import url

from forms.ajax import FormAjaxValidator, CompositeAjaxFormValidator
from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm, PermissionsForm
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
    url(r'^!action:change-folder/$', actions_views.change_folder, name="action-change-folder"),
    url(r'^!action:delete/$', actions_views.delete, name="action-delete"),
    url(r'^!action:copy/$', actions_views.delete, name="action-copy"),
    url(r'^!action:cut/$', actions_views.delete, name="action-cut"),
    url(r'^!action:paste/$', actions_views.delete, name="action-paste"),
]

# Form validators
urlpatterns += [
    url(r'^!validator:create-folders/$',
        CompositeAjaxFormValidator.as_view(forms=[CreateFolderForm, PermissionsForm]),
        name="validator-create-folders"),

    url(r'^!validator:create-documents/$', FormAjaxValidator.as_view(form=CreateDocumentForm),
        name="validator-create-documents"),
]
