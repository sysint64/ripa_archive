from io import UnsupportedOperation

from django.core.exceptions import SuspiciousOperation
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from ripa_archive.activity import activity_factory
from ripa_archive.documents import strings
from ripa_archive.documents.forms.browser import CreateFolderForm, CreateDocumentForm, \
    FolderPermissionsCreateForm, DocumentPermissionsCreateForm, FolderPermissionsEditForm, \
    DocumentPermissionsEditForm
from ripa_archive.documents.models import Document, FolderCustomPermission, \
    DocumentCustomPermission
from ripa_archive.documents.views.main import get_folder_or_404, browser_base_context
from ripa_archive.documents.views.single.main import get_document
from ripa_archive.views import MultiFormCreationWithPermissions, MultiFormView


class BrowserMultiFormCreation(MultiFormCreationWithPermissions):
    def get_context_data(self, **kwargs):
        path = kwargs.get("path")
        parent_folder = get_folder_or_404(path)

        context = super().get_context_data(**kwargs)
        context.update(browser_base_context(self.request))
        context.update({
            "parent_folder": parent_folder,
        })

        return context

    # TODO: reduce repetition - path, parent_folder
    def get_forms(self, **kwargs):
        path = kwargs.get("path")
        parent_folder = get_folder_or_404(path)
        return [self.form_class(initial={"parent": parent_folder})]

    def get_pattern_form(self, **kwargs):
        path = kwargs.get("path")
        parent_folder = get_folder_or_404(path)
        return self.form_class(initial={"parent": parent_folder})

    def post(self, request, **kwargs):
        path = kwargs.get("path")
        self.parent_folder = get_folder_or_404(path)
        return super().post(request, **kwargs)

    def perform_save(self, form):
        item = form.save(commit=False)
        item.parent = self.parent_folder
        item.save()
        return item

    def do_redirect(self, redirect_url_name, **kwargs):
        path = kwargs.get("path")

        if path is None:
            return redirect("documents:%s" % redirect_url_name)
        else:
            return redirect("documents:%s" % redirect_url_name, path=path)


class CreateFolders(BrowserMultiFormCreation):
    title = _("Create folders")
    validator_url = "documents:validator-create-folders"
    form_class = CreateFolderForm
    permissions_form_class = FolderPermissionsCreateForm
    redirect_url_name = "create-folders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "submit_title": _("Create"),
            "add_title": _("Add another folder")
        })
        return context

    def perform_save(self, form):
        folder = super().perform_save(form)
        activity_factory.for_folder(
            self.request.user,
            folder,
            strings.i18n_format(
                strings.ACTIVITY_CREATE_FOLDER,
                name=folder.name,
                path=folder.path
            )
        )

        return folder


class CreateDocuments(BrowserMultiFormCreation):
    title = _("Create documents")
    validator_url = "documents:validator-create-documents"
    form_class = CreateDocumentForm
    permissions_form_class = DocumentPermissionsCreateForm
    redirect_url_name = "create-documents"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "submit_title": _("Create"),
            "add_title": _("Add another document")
        })
        return context

    def perform_save(self, form):
        document = Document.objects.create(
            owner=self.request.user,
            parent=form.cleaned_data["parent"],
            name=form.cleaned_data["name"],
            status=form.cleaned_data["status"]
        )
        data = form.save(commit=False)
        data.document = document
        data.save()

        document.data = document.last_data
        document.owner = self.request.user
        document.followers.add(self.request.user)
        document.save()

        activity_factory.for_document(
            self.request.user,
            document,
            strings.i18n_format(
                strings.ACTIVITY_CREATE_DOCUMENT,
                name=document.name,
                path=document.path
            ),
            document_data=document.last_data
        )

        return document


class EditPermissions(MultiFormView):
    title = _("Edit permissions")
    form_class = None
    instance_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "submit_title": _("Update permissions"),
            "add_title": _("Add another permission")
        })
        return context

    def get_for_instance(self, **kwargs):
        raise UnsupportedOperation()

    def get_queryset(self, for_instance):
        return self.instance_class.objects.filter(for_instance=for_instance)

    def get_forms(self, **kwargs):
        for_instance = self.get_for_instance(**kwargs)
        forms = []

        # permissions = self.instance_class.objects.filter(for_instance=for_instance)
        permissions = self.get_queryset(for_instance)

        for index, permission in enumerate(permissions):
            prefix = "block" + str(index) if index != 0 else ""
            forms.append(self.form_class(instance=permission, prefix=prefix))

        return forms

    def perform_delete(self, instance, **kwargs):
        for_instance = self.get_for_instance(**kwargs)

        # TODO: uncomment
        # if instance.for_instance != for_instance:
        #     raise SuspiciousOperation()

        instance.delete()

    def get_pattern_form(self, **kwargs):
        return self.form_class(initial={
            "for_instance": self.get_for_instance(**kwargs)
        })


class EditFolderPermissions(EditPermissions):
    form_class = FolderPermissionsEditForm
    instance_class = FolderCustomPermission
    validator_url = "documents:validator-edit-folder-permissions"

    def get_for_instance(self, **kwargs):
        path = kwargs.get("path")
        return get_folder_or_404(path)


class EditDocumentPermissions(EditPermissions):
    form_class = DocumentPermissionsEditForm
    instance_class = DocumentCustomPermission
    validator_url = "documents:validator-edit-document-permissions"

    def get_for_instance(self, **kwargs):
        return get_document(**kwargs)
