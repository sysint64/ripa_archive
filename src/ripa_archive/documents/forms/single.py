from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from forms.ajax import AjaxModelForm
from ripa_archive.documents import validators
from ripa_archive.documents.models import DocumentData, Folder, Remark, Document, FoldersManager, \
    DocumentsManager


class UploadNewVersionForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "file",

    parent = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )
    name = forms.CharField(label=_("Name"), max_length=255)
    message = forms.CharField(
        label=_("Details"),
        help_text=_("What was done in this revision"),
        required=True,
        widget=forms.Textarea(attrs={"rows": 2})
    )

    file = forms.FileField(
        label=_("File"),
        help_text=_("New version of document")
    )

    # Check uniqueness in folder
    def clean_name(self):
        name = self.cleaned_data["name"]
        parent = self.cleaned_data["parent"]

        if Document.objects.exist_with_name(parent, name):
            raise ValidationError(DocumentsManager.ALREADY_EXIST_ERROR % name)

        return name


class RenameFolderForm(AjaxModelForm):
    class Meta:
        model = Folder
        fields = "parent", "name"

    parent = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        required=True,
        widget=forms.HiddenInput()
    )
    name = forms.CharField(
        validators=[validators.name_validator],
        max_length=validators.NAME_MAX_LENGTH,
        required=True,
        label=_("Name")
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
    name = forms.CharField(
        validators=[validators.name_validator],
        max_length=validators.NAME_MAX_LENGTH,
        required=True,
        label=_("Name")
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
        label=_("Remark"),
        required=True,
        widget=forms.Textarea(attrs={"rows": 2})
    )


class UpdateStatusForm(AjaxModelForm):
    class Meta:
        model = Document
        fields = "status",
