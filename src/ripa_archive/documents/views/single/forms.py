from django.contrib import messages
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.translation import ugettext_lazy as _

from request_helper import get_request_int_or_404
from ripa_archive.activity import activity_factory
from ripa_archive.documents import strings
from ripa_archive.documents.forms.single import UploadNewVersionForm, RemarkForm, RenameDocumentForm, \
    RenameFolderForm, UpdateStatusForm
from ripa_archive.documents.models import Remark
from ripa_archive.documents.views.main import browser_base_context
from ripa_archive.documents.views.single.main import get_document, get_folder
from ripa_archive.notifications import notifications_factory
from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_TAKE_DOCUMENT_FOR_REVISION], get_instance_functor=get_document)
def upload_new_version(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.current_edit_meta is None:
        raise PermissionDenied()

    if request.method == "POST":
        # No instance because need new version of document and save old version
        form = UploadNewVersionForm(request.POST, request.FILES)
    else:
        form = UploadNewVersionForm(
            instance=document.data,
            initial={"name": name, "parent": document.parent}
        )

    context = browser_base_context(request)
    context.update({
        "form_title": _("Upload new version"),
        "form": form,
        "submit_title": _("Upload"),
        "validator_url": reverse("documents:validator-upload-new-version"),
    })

    if request.method == "POST" and form.is_valid():
        data = form.save(commit=False)
        data.document = document
        data.save()

        document.data = data

        activity_factory.for_document(
            request.user,
            document,
            form.cleaned_data["message"],
            document_data=data
        )

        if document.name != form.cleaned_data["name"]:
            document.name = form.cleaned_data["name"]
            activity_factory.for_document(
                request.user,
                document,
                strings.i18n_format(
                    strings.ACTIVITY_RENAME_DOCUMENT,
                    old_name=document.name,
                    new_name=form.cleaned_data["name"]
                )
            )

        document.save()
        messages.success(request, _("Successfully uploaded"))
        return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_REVIEW], get_instance_functor=get_document)
def write_remark(request, name, path=None):
    document = get_document(name=name, path=path)
    reject_remark_id = request.GET.get("reject_remark_id")
    remark_to_reject = None

    if reject_remark_id is not None:
        reject_remark_id = get_request_int_or_404(request, "GET", "reject_remark_id")
        remark_to_reject = get_object_or_404(Remark, id=reject_remark_id)

        if remark_to_reject.is_rejected:
            raise PermissionDenied()

    if document.current_edit_meta is None:
        raise PermissionDenied()

    form = RemarkForm(request.POST)

    context = browser_base_context(request)
    context.update({
        "form_title": _("Write remark"),
        "form": form,
        "submit_title": _("Submit"),
        "validator_url": reverse("documents:validator-write-remark"),
    })

    if request.method == "POST" and form.is_valid():
        remark = form.save(commit=False)
        remark.edit_meta = document.current_edit_meta
        remark.user = request.user
        remark.save()

        # Reject remark
        if remark_to_reject is not None:
            remark_to_reject.status = Remark.Status.REJECTED
            remark_to_reject.save()

            notifications_factory.notification_remark(
                request.user,
                document,
                remark_to_reject,
                strings.NOTIFICATION_REMARK_REJECTED
            )

        notifications_factory.notification_remark(
            request.user,
            document,
            remark,
            strings.NOTIFICATION_REMARK_WROTE
        )

        messages.success(request, _("Successfully submitted remark"))
        return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_EDIT], get_instance_functor=get_document)
def rename_document(request, name, path=None):
    document = get_document(name=name, path=path)
    old_name = document.name

    if request.method == "POST":
        form = RenameDocumentForm(request.POST, instance=document)
    else:
        form = RenameDocumentForm(instance=document)

    context = browser_base_context(request)
    context.update({
        "form_title": _("Rename document"),
        "form": form,
        "submit_title": _("Rename"),
        "validator_url": reverse("documents:validator-rename-document"),
    })

    if request.method == "POST" and form.is_valid():
        redirect_next = request.GET.get("next", "single")

        if old_name != document.name:
            activity_factory.for_document(
                request.user,
                document,
                strings.i18n_format(
                    strings.ACTIVITY_RENAME_DOCUMENT,
                    old_name=old_name,
                    new_name=document.name
                )
            )

        form.save()
        messages.success(request, _("Successfully renamed"))

        if redirect_next == "list":
            return redirect(document.parent.permalink)
        else:
            return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.FOLDERS_CAN_EDIT], get_instance_functor=get_folder)
def rename_folder(request, path=None):
    folder = get_folder(path=path)
    old_name = folder.name

    if request.method == "POST":
        form = RenameFolderForm(request.POST, instance=folder)
    else:
        form = RenameFolderForm(instance=folder)

    context = browser_base_context(request)
    context.update({
        "form_title": _("Rename folder"),
        "form": form,
        "submit_title": _("Rename"),
        "validator_url": reverse("documents:validator-rename-folder"),
    })

    if request.method == "POST" and form.is_valid():
        redirect_next = request.GET.get("next", "list")

        if old_name != form.cleaned_data["name"]:
            activity_factory.for_folder(
                request.user,
                folder,
                strings.i18n_format(
                    strings.ACTIVITY_RENAME_FOLDER,
                    old_name=old_name,
                    new_name=form.cleaned_data["name"]
                )
            )

        form.save()

        messages.success(request, _("Successfully renamed"))

        if redirect_next == "list":
            return redirect(folder.parent.permalink)
        else:
            return redirect(folder.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_EDIT], get_instance_functor=get_document)
def update_document_status(request, name, path=None):
    document = get_document(name=name, path=path)

    if request.method == "POST":
        form = UpdateStatusForm(request.POST, instance=document)
    else:
        form = UpdateStatusForm(instance=document)

    context = browser_base_context(request)
    context.update({
        "form_title": _("Update document status"),
        "form": form,
        "submit_title": _("Update"),
        "validator_url": reverse("documents:validator-update-document-status"),
    })

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Successfully updated"))
        return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)
