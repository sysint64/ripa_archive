from django.shortcuts import redirect
from django.db import transaction

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
        item = form.save(commit=False)
        item.document = document
        item.save()

        document.data = document.last_data
        document.save()
