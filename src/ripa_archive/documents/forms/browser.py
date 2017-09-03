from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from forms.ajax import AjaxModelForm
from ripa_archive.accounts.models import User
from ripa_archive.documents import validators
from ripa_archive.documents.models import Folder, DocumentData, FolderCustomPermission, \
    DocumentCustomPermission, Document, FoldersManager, DocumentsManager
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


class CreateDocumentForm(AjaxModelForm):
    class Meta:
        model = DocumentData
        fields = "file",

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
    status = forms.ChoiceField(choices=Document.Status.FORM_CHOICES, label="Status")

    # Check uniqueness in folder
    def clean_name(self):
        name = self.cleaned_data["name"]
        parent = self.cleaned_data["parent"]

        if Document.objects.exist_with_name(parent, name):
            raise ValidationError(DocumentsManager.ALREADY_EXIST_ERROR % name)

        return name


class PermissionsFormMixin:
    users_attrs = {
        "label": _("Users"),
        "queryset": User.objects.all(),
        "widget": forms.SelectMultiple(attrs={
            "data-actions-box": "true",
            "data-width": "fit",
            "data-live-search": "true"
        }),
        "required": False,
    }

    groups_attrs = {
        "label": _("Groups"),
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
            "label": _("Permissions"),
            "widget": forms.CheckboxSelectMultiple(),
            "required": False,
            "queryset": queryset,
        }

    def clean(self):
        users = self.cleaned_data["users"]
        groups = self.cleaned_data["groups"]

        if users.count() == 0 and groups.count() == 0:
            self.add_error("groups", _("At least one field must be filled in"))
            self.add_error("users", "")

        return self.cleaned_data


class FolderPermissionsCreateForm(PermissionsFormMixin, AjaxModelForm):
    class Meta:
        model = FolderCustomPermission
        fields = "groups", "users", "permissions",

    users = forms.ModelMultipleChoiceField(**PermissionsFormMixin.users_attrs)
    groups = forms.ModelMultipleChoiceField(**PermissionsFormMixin.groups_attrs)
    permissions = forms.ModelMultipleChoiceField(
        **PermissionsFormMixin.permissions_attrs(Permission.objects.for_folders()),
    )


class DocumentPermissionsCreateForm(PermissionsFormMixin, AjaxModelForm):
    class Meta:
        model = DocumentCustomPermission
        fields = "groups", "users", "permissions",

    users = forms.ModelMultipleChoiceField(**PermissionsFormMixin.users_attrs)
    groups = forms.ModelMultipleChoiceField(**PermissionsFormMixin.groups_attrs)
    permissions = forms.ModelMultipleChoiceField(
        **PermissionsFormMixin.permissions_attrs(Permission.objects.for_documents()),
    )


class FolderPermissionsEditForm(PermissionsFormMixin, AjaxModelForm):
    class Meta:
        model = FolderCustomPermission
        fields = "for_instance", "groups", "users", "permissions",

    for_instance = forms.ModelChoiceField(
        queryset=Folder.objects.all(),
        widget=forms.HiddenInput
    )
    users = forms.ModelMultipleChoiceField(**PermissionsFormMixin.users_attrs)
    groups = forms.ModelMultipleChoiceField(**PermissionsFormMixin.groups_attrs)
    permissions = forms.ModelMultipleChoiceField(
        **PermissionsFormMixin.permissions_attrs(Permission.objects.for_folders()),
    )


class DocumentPermissionsEditForm(PermissionsFormMixin, AjaxModelForm):
    class Meta:
        model = DocumentCustomPermission
        fields = "for_instance", "groups", "users", "permissions",

    for_instance = forms.ModelChoiceField(
        queryset=Document.objects.all(),
        widget=forms.HiddenInput
    )
    users = forms.ModelMultipleChoiceField(**PermissionsFormMixin.users_attrs)
    groups = forms.ModelMultipleChoiceField(**PermissionsFormMixin.groups_attrs)
    permissions = forms.ModelMultipleChoiceField(
        **PermissionsFormMixin.permissions_attrs(Permission.objects.for_documents()),
    )
