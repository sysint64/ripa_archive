from forms.ajax import AjaxModelForm
from ripa_archive.labels.models import Label


class LabelForm(AjaxModelForm):
    class Meta:
        model = Label
        fields = "code", "name", "hex_color"
