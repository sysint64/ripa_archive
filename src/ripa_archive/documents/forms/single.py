from django import forms
from forms.ajax import AjaxModelForm
from ripa_archive.documents.models import DocumentData, Folder, Remark


class UploadNewVersionForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "name", "file",

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


class RenameFolder(AjaxModelForm):
    class Meta:
        model = Folder
        fields = "name",


class RenameDocument(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "name",


class RemarkForm(AjaxModelForm):
    class Meta:
        model = Remark
        fields = "text",

    text = forms.CharField(
        label="Remark",
        required=True,
        widget=forms.Textarea(attrs={"rows": 2})
    )
