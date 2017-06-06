from django import forms
from forms.ajax import AjaxModelForm, AjaxForm
from ripa_archive.documents.models import Folder, DocumentData, Status


class CreateFolderForm(AjaxModelForm):
    class Meta:
        model = Folder
        fields = "name",


class CreateDocumentForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "name", "file",

    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Status")


class PermissionsForm(AjaxModelForm):
    pass
