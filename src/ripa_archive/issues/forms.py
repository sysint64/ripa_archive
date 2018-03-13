from django import forms
from django.utils.translation import ugettext_lazy as _

from forms.ajax import AjaxModelForm
from ripa_archive.documents import validators
from ripa_archive.issues.models import Issue, IssueItem, Remark


class CreateIssueForm(AjaxModelForm):
    class Meta:
        model = Issue
        fields = "name",

    name = forms.CharField(
        validators=[validators.name_validator],
        max_length=validators.NAME_MAX_LENGTH,
        required=True,
        label=_("Name")
    )


class CreateIssueWithOwnerForm(AjaxModelForm):
    class Meta:
        model = Issue
        fields = "owner", "name",

    name = forms.CharField(
        validators=[validators.name_validator],
        max_length=validators.NAME_MAX_LENGTH,
        required=True,
        label=_("Name")
    )


class IssueItemForm(AjaxModelForm):
    class Meta:
        model = IssueItem
        fields = "name", "content"

    name = forms.CharField(
        validators=[validators.name_validator],
        max_length=validators.NAME_MAX_LENGTH,
        required=True,
        label=_("Name")
    )


class RemarkForm(AjaxModelForm):
    class Meta:
        model = Remark
        fields = "text",

    text = forms.CharField(
        label=_("Remark"),
        required=True,
        widget=forms.Textarea(attrs={"rows": 2})
    )
