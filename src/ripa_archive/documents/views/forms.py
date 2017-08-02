from django.shortcuts import redirect
from django.db import transaction

from ripa_archive.activity.models import Activity
from ripa_archive.documents import strings
from ripa_archive.documents.forms.browser import CreateFolderForm, CreateDocumentForm, \
    FolderPermissionsForm, DocumentPermissionsForm
from ripa_archive.documents.models import Document
from ripa_archive.documents.views.main import get_folder_or_404
from ripa_archive.views import MultiFormCreationWithPermissions


class BrowserMultiFormCreation(MultiFormCreationWithPermissions):
    def get_context_data(self, **kwargs):
        path = kwargs.get("path")
        parent_folder = get_folder_or_404(path)

        context = super().get_context_data(**kwargs)
        context.update({
            "parent_folder": parent_folder,
            "form": self.form_class(initial={"parent": parent_folder}),
        })

        return context

    @transaction.atomic
    def post(self, request, **kwargs):
        path = kwargs.get("path")
        self.parent_folder = get_folder_or_404(path)
        return super().post(request, **kwargs)

    def perform_create(self, form):
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
    title = "Create folders"
    validator_url = "documents:validator-create-folders"
    form_class = CreateFolderForm
    permissions_form_class = FolderPermissionsForm
    redirect_url_name = "create-folders"

    def perform_create(self, form):
        folder = super().perform_create(form)
        Activity.objects.create(
            user=self.request.user,
            content_type="documents.Folder",
            target_id=folder.pk,
            details=strings.ACTIVITY_CREATE_FOLDER.format(
                name=folder.name,
                path=folder.path
            )
        )
        return folder


class CreateDocuments(BrowserMultiFormCreation):
    title = "Create documents"
    validator_url = "documents:validator-create-documents"
    form_class = CreateDocumentForm
    permissions_form_class = DocumentPermissionsForm
    redirect_url_name = "create-documents"

    def perform_create(self, form):
        document = Document.objects.create(
            parent=self.parent_folder,
            owner=self.request.user,
            status=form.cleaned_data["status"]
        )
        data = form.save(commit=False)
        data.document = document
        data.save()

        document.data = document.last_data
        document.save()

        Activity.objects.create(
            user=self.request.user,
            content_type="documents.Document",
            target_id=document.pk,
            document_data=document.data,
            details=strings.ACTIVITY_CREATE_DOCUMENT.format(
                name=document.data.name,
                path=document.path
            )
        )
