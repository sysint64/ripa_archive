from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.db import transaction

from forms.multi_form import get_multi_form
from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm, \
    FolderPermissionsForm, DocumentPermissionsForm
from ripa_archive.documents.models import Document
from ripa_archive.documents.views.main import get_folder_or_404, BROWSER_SEARCH_PLACES


def browser_redirect(name, path=None):
    if path is None:
        return redirect("documents:%s" % name)
    else:
        return redirect("documents:%s" % name, path=path)


class MultiFormCreation(View):
    title = ""
    validator_url = None
    form_class = None
    permissions_form_class = None
    redirect_url_name = ""

    def get(self, request, path=None):
        parent_folder = get_folder_or_404(path)
        context = {
            "parent_folder": parent_folder,
            "form_title": self.title,
            "validator_url": reverse(self.validator_url),
            "search_places": BROWSER_SEARCH_PLACES,
            "form": self.form_class(initial={"parent": parent_folder}),
            "permissions_form": self.permissions_form_class(),
            "form_prefixes_field": self.form_class.prefixes_field("form_prefixes"),
            "permissions_form_prefixes_field": self.permissions_form_class.prefixes_field("permissions_form_prefixes"),
        }
        return TemplateResponse(request=request, template="forms/multi-form-permissions.html", context=context)

    @transaction.atomic
    def post(self, request, path=None):
        self.parent_folder = get_folder_or_404(path)
        forms = get_multi_form(self.form_class, request.POST, self.request.FILES)
        permissions_forms = get_multi_form(self.permissions_form_class, request.POST, self.request.FILES, ignore_first=True)

        for form in forms:
            if not form.is_valid():
                messages.error(request, form.errors)
                return browser_redirect(self.redirect_url_name, path)

        for form in permissions_forms:
            if not form.is_valid():
                messages.error(request, form.errors)
                return browser_redirect(self.redirect_url_name, path)

        instances = []

        # All forms are valid
        for form in forms:
            item = self.perform_create(form)
            instances.append(item)

        for form in permissions_forms:
            print(form.cleaned_data)
            self.perform_permissions_create(form, instances)

        return browser_redirect("browser", path)

    def perform_create(self, form):
        item = form.save(commit=False)
        item.parent = self.parent_folder
        item.save()
        return item

    def perform_permissions_create(self, form, for_instances):
        permission = form.save()

        for instance in for_instances:
            permission.for_instances.add(instance)


class CreateFolders(MultiFormCreation):
    title = "Create folders"
    validator_url = "documents:validator-create-folders"
    form_class = CreateFolderForm
    permissions_form_class = FolderPermissionsForm
    redirect_url_name = "create-folders"


class CreateDocuments(MultiFormCreation):
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
