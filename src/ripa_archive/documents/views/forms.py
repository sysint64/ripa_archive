from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.db import transaction

from forms.multi_form import get_multi_form
from ripa_archive.documents.forms import CreateFolderForm, CreateDocumentForm, PermissionsForm
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

    def get(self, request, path=None):
        parent_folder = get_folder_or_404(path)
        context = {
            "parent_folder": parent_folder,
            "form_title": self.title,
            "validator_url": reverse(self.validator_url),
            "search_places": BROWSER_SEARCH_PLACES,
            "form": self.form_class(initial={"parent": parent_folder}),
            "permissions_form": PermissionsForm(),
            "form_prefixes_field": self.form_class.prefixes_field("form_prefixes"),
            "permissions_form_prefixes_field": PermissionsForm.prefixes_field("permissions_form_prefixes"),
        }
        return TemplateResponse(request=request, template="forms/multi-form-permissions.html", context=context)

    @transaction.atomic
    def post(self, request, path=None):
        self.parent_folder = get_folder_or_404(path)
        forms = get_multi_form(self.form_class, request.POST)
        permissions_forms = get_multi_form(self.permissions_form_class, request.POST, ignore_first=True)

        print(request.POST)
        # print(permissions_forms)

        for form in forms:
            if not form.is_valid():
                messages.error(request, form.errors)
                return browser_redirect("create-folders", path)

        for form in permissions_forms:
            if not form.is_valid():
                messages.error(request, form.errors)
                return browser_redirect("create-folders", path)

        instances = []

        # All forms are valid
        for form in forms:
            item = self.perform_create(form.save(commit=False))
            instances.append(item)

        for form in permissions_forms:
            print(form.cleaned_data)
            self.perform_permissions_create(form.save(), instances)

        return browser_redirect("browser", path)

    def perform_create(self, item):
        item.parent = self.parent_folder
        item.save()
        return item

    def perform_permissions_create(self, permission, for_instances):
        for instance in for_instances:
            permission.for_instances.add(instance)


class CreateFolders(MultiFormCreation):
    title = "Create folders"
    validator_url = "documents:validator-create-folders"
    form_class = CreateFolderForm
    permissions_form_class = PermissionsForm


class CreateDocuments(MultiFormCreation):
    title = "Create documents"
    validator_url = "documents:validator-create-documents"
    form_class = CreateDocumentForm
