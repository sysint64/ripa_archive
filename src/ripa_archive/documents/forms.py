from django import forms
from django.core.exceptions import ValidationError

from forms.ajax import AjaxModelForm, AjaxForm
from ripa_archive.documents.models import Folder, DocumentData, Status


class CreateFolderForm(AjaxModelForm):
    class Meta:
        model = Folder
        fields = "parent", "name",

    parent = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )

    # Check uniqueness in folder
    def clean_name(self):
        name = self.cleaned_data["name"]
        parent = self.cleaned_data["parent"]

        if Folder.objects.filter(parent=parent, name=name).count() > 0:
            raise ValidationError("Folder with this name already exist")

        return name


class CreateDocumentForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "name", "file",

    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Status")


class PermissionsForm(AjaxModelForm):
    pass
