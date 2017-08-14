from django import forms
from django.forms.widgets import Input

from forms.ajax import AjaxModelForm
from ripa_archive.permissions.models import Group, Permission


class GroupForm(AjaxModelForm):
    class Meta:
        model = Group
        fields = "inherit", "name"

    inherit = forms.ModelMultipleChoiceField(
        label="Inherit from",
        required=False,
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={
            "data-actions-box": "true",
            "data-width": "fit",
            "data-live-search": "true"
        }),
    )

    common_permissions = forms.ModelMultipleChoiceField(
        label="Common permissions",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        queryset=Permission.objects.common(),
    )

    folder_permissions = forms.ModelMultipleChoiceField(
        label="Folder permissions",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        queryset=Permission.objects.for_generic_folders(),
    )

    documents_permissions = forms.ModelMultipleChoiceField(
        label="Documents permissions",
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        queryset=Permission.objects.for_generic_documents(),
    )

    @property
    def permissions(self):
        return self.cleaned_data["folder_permissions"] | self.cleaned_data["documents_permissions"] | self.cleaned_data["common_permissions"]

    @staticmethod
    def initial(instance):
        return {
            "folder_permissions": instance.permissions.all(),
            "documents_permissions": instance.permissions.all(),
            "common_permissions": instance.permissions.all(),
        }