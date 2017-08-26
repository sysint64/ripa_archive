from django import forms
from django.core.exceptions import ValidationError, SuspiciousOperation

from forms.ajax import AjaxModelForm
from ripa_archive.documents.models import DocumentData, Folder, Remark, Document, FoldersManager, \
    DocumentsManager


class UploadNewVersionForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "file",

    name = forms.CharField(max_length=255)
    message = forms.CharField(
        label="Details",
        help_text="What was done in this revision",
        required=True,
        widget=forms.Textarea(attrs={"rows": 2})
    )

    file = forms.FileField(
        label="File",
        help_text="New version of document"
    )


class RenameFolderForm(AjaxModelForm):
    class Meta:
        model = Folder
        fields = "parent", "name"

    parent = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )

    # Check uniqueness in folder
    def clean_name(self):
        name = self.cleaned_data["name"]
        parent = self.cleaned_data["parent"]

        if Folder.objects.exist_with_name(parent, name):
            raise ValidationError(FoldersManager.ALREADY_EXIST_ERROR % name)

        return name


class RenameDocumentForm(AjaxModelForm):
    class Meta:
        model = Document
        fields = "parent", "name"

    parent = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        required=True,
        widget=forms.HiddenInput(),
    )

    # Check uniqueness in folder
    def clean_name(self):
        name = self.cleaned_data["name"]
        parent = self.cleaned_data["parent"]

        if Document.objects.exist_with_name(parent, name):
            raise ValidationError(DocumentsManager.ALREADY_EXIST_ERROR % name)

        return name


class RemarkForm(AjaxModelForm):
    class Meta:
        model = Remark
        fields = "text",

    text = forms.CharField(
        label="Remark",
        required=True,
        widget=forms.Textarea(attrs={"rows": 2})
    )


class UpdateStatusForm(AjaxModelForm):
    class Meta:
        model = Document
        fields = "status",
