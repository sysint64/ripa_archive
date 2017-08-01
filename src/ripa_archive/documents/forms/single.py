from forms.ajax import AjaxModelForm
from ripa_archive.documents.models import DocumentData


class UploadNewVersionForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "name", "file",
