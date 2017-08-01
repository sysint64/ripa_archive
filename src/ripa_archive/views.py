import os

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_text, smart_str
from django.views import View
from django.contrib import messages
from django.views.static import serve

from forms.multi_form import get_multi_form
from urllib.parse import quote


def layout(request, template):
    return render_to_response("layout/{}.html".format(template))


class MultiFormCreation(View):
    title = ""
    validator_url = None
    form_class = None
    redirect_url_name = ""
    template = "forms/multi-form.html"

    def get_context_data(self, **kwargs):
        return {
            "form_title": self.title,
            "validator_url": reverse(self.validator_url),
            "form": self.form_class(),
            "form_prefixes_field": self.form_class.prefixes_field("form_prefixes"),
        }

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return TemplateResponse(request=request, template=self.template, context=context)

    @transaction.atomic
    def post(self, request, **kwargs):
        success, _ = self.perform_form(request, **kwargs)

        if success:
            return self.do_redirect("index", **kwargs)
        else:
            return self.do_redirect(self.redirect_url_name, **kwargs)

    def do_redirect(self, redirect_url_name, **kwargs):
        return redirect(redirect_url_name)

    def perform_form(self, request, **kwargs):
        forms = get_multi_form(self.form_class, request.POST, self.request.FILES)

        for form in forms:
            if not form.is_valid():
                messages.error(request, form.errors)
                return False, None

        instances = []

        for form in forms:
            item = self.perform_create(form)
            instances.append(item)

        return True, instances

    def perform_create(self, form):
        item = form.save()
        return item


class MultiFormCreationWithPermissions(MultiFormCreation):
    permissions_form_class = None
    template = "forms/multi-form-permissions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "permissions_form": self.permissions_form_class(),
            "permissions_form_prefixes_field": self.permissions_form_class.prefixes_field("permissions_form_prefixes"),
        })

        return context

    @transaction.atomic
    def post(self, request, **kwargs):
        success, instances = self.perform_form(request, **kwargs)

        if not success:
            return self.do_redirect(self.redirect_url_name, **kwargs)

        success, _ = self.perform_permissions_form(request, instances, **kwargs)

        if not success:
            return self.do_redirect(self.redirect_url_name, **kwargs)

        return self.do_redirect("index", **kwargs)

    def perform_permissions_form(self, request, form_instances, **kwargs):
        permissions_forms = get_multi_form(self.permissions_form_class, request.POST,
                                           self.request.FILES, ignore_first=True)

        for form in permissions_forms:
            if not form.is_valid():
                messages.error(request, form.errors)
                return False, None

        permissions = []

        for form in permissions_forms:
            item = self.perform_permissions_create(form, form_instances)
            permissions.append(item)

        return True, permissions

    def perform_permissions_create(self, form, for_instances):
        permission = form.save()

        for instance in for_instances:
            permission.for_instances.add(instance)

        return permission


def sendfile(request, filename, force_download=False):
    def _convert_file_to_url(filename):
        relpath = os.path.relpath(filename, settings.PROTECTED_FILES_ROOT)
        url = [settings.PROTECTED_FILES_URL]

        while relpath:
            relpath, head = os.path.split(relpath)
            url.insert(1, head)

        url = [smart_bytes(url_component) for url_component in url]
        return smart_text(quote(b'/'.join(url)))

    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)

    if settings.DEBUG:
        response = serve(request, basename, dirname)
    else:
        # TODO: X-Accel
        response = HttpResponse()
        url = _convert_file_to_url(filename)
        response["X-Accel-Redirect"] = url.encode("utf-8")

    if force_download:
        response["Content-Type"] = "application/force-download"
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(basename)
    else:
        response['Content-Disposition'] = 'filename=%s' % smart_str(basename)

    return response
