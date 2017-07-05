from django import forms
from django.core.exceptions import ValidationError

from forms.ajax import AjaxModelForm
from ripa_archive.accounts.models import User
from ripa_archive.documents.models import Folder, DocumentData, Status, FolderCustomPermission, \
    DocumentCustomPermission
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


class PermissionsFormMixin:
    users_attrs = {
        "label": "Users",
        "queryset": User.objects.all(),
        "widget": forms.SelectMultiple(attrs={
            "data-actions-box": "true",
            "data-width": "fit",
            "data-live-search": "true"
        }),
        "required": False,
    }

    groups_attrs = {
        "label": "Groups",
        "queryset": Group.objects.all(),
        "widget": forms.SelectMultiple(attrs={
            "data-actions-box": "true",
            "data-width": "fit",
            "data-live-search": "true"
        }),
        "required": False,
    }

    @staticmethod
    def permissions_attrs(queryset):
        return {
            "label": "Permissions",
            "widget": forms.CheckboxSelectMultiple(),
            "required": True,
            "queryset": queryset,
        }

    def clean(self):
        users = self.cleaned_data["users"]
        groups = self.cleaned_data["groups"]

        if users.count() == 0 and groups.count() == 0:
            self.add_error("groups", "At least one field must be filled in")
            self.add_error("users", "")

        return self.cleaned_data


class FolderPermissionsForm(PermissionsFormMixin, AjaxModelForm):
    class Meta:
        model = FolderCustomPermission
        fields = "groups", "users", "permissions",

    users = forms.ModelMultipleChoiceField(**PermissionsFormMixin.users_attrs)
    groups = forms.ModelMultipleChoiceField(**PermissionsFormMixin.groups_attrs)
    permissions = forms.ModelMultipleChoiceField(
        **PermissionsFormMixin.permissions_attrs(Permission.objects.for_folders()),
    )


class DocumentPermissionsForm(PermissionsFormMixin, AjaxModelForm):
    class Meta:
        model = DocumentCustomPermission
        fields = "groups", "users", "permissions",

    users = forms.ModelMultipleChoiceField(**PermissionsFormMixin.users_attrs)
    groups = forms.ModelMultipleChoiceField(**PermissionsFormMixin.groups_attrs)
    permissions = forms.ModelMultipleChoiceField(
        **PermissionsFormMixin.permissions_attrs(Permission.objects.for_documents()),
    )
