from django import forms
from django.core.exceptions import ValidationError

from forms.ajax import AjaxModelForm, AjaxForm
from ripa_archive.accounts.models import User
from ripa_archive.documents.models import Folder, DocumentData, Status, FolderCustomPermission
from ripa_archive.permissions.models import Permission, Group


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

        if Folder.objects.filter(parent=parent, name__iexact=name).count() > 0:
            raise ValidationError("Folder with this name already exist")

        return name


class CreateDocumentForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "name", "file",

    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Status")


class PermissionsForm(AjaxModelForm):
    class Meta:
        model = FolderCustomPermission
        fields = "groups", "users", "permissions",

    users = forms.ModelMultipleChoiceField(
        label="Users",
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "selectpicker",
            "data-actions-box": "true",
            "data-width": "fit",
            "data-live-search": "true"
        })
    )

    groups = forms.ModelMultipleChoiceField(
        label="Groups",
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "class": "selectpicker",
            "data-actions-box": "true",
            "data-width": "fit",
            "data-live-search": "true"
        })
    )

    permissions = forms.ModelMultipleChoiceField(
        label="Permissions",
        queryset=Permission.objects.for_folders(),
        widget=forms.CheckboxSelectMultiple()
    )
