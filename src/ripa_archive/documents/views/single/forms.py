from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ripa_archive.activity.models import Activity
from ripa_archive.documents import strings
from ripa_archive.documents.forms.single import UploadNewVersionForm, RemarkForm, RenameDocument, \
    RenameFolder
from ripa_archive.documents.models import Document, Folder, Remark
from ripa_archive.documents.views.main import get_folder_or_404, browser_base_context
from ripa_archive.notifications import notifications_factory


@require_http_methods(["GET", "POST"])
@transaction.atomic
def upload_new_version(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)

    if document.current_edit_meta is None:
        raise PermissionDenied()

    if request.method == "POST":
        # No instance because need new version of document and save old version
        form = UploadNewVersionForm(request.POST, request.FILES)
    else:
        form = UploadNewVersionForm(instance=document.data)

    context = browser_base_context(request)
    context.update({
        "form_title": "Upload new version",
        "form": form,
        "submit_title": "Upload",
        "validator_url": reverse("documents:validator-upload-new-version"),
    })

    if request.method == "POST" and form.is_valid():
        data = form.save(commit=False)
        data.document = document
        data.save()

        Activity.objects.create_for_document(
            request.user,
            document,
            user=request.user,
            content_type=Document.content_type,
            target_id=document.pk,
            document_data=data,
            details=form.cleaned_data["message"]
        )

        if document.name != form.cleaned_data["name"]:
            Activity.objects.create_for_document(
                request.user,
                document,
                user=request.user,
                content_type=Document.content_type,
                target_id=document.pk,
                details=strings.ACTIVITY_RENAME_DOCUMENT.format(
                    old_name=document.name,
                    new_name=form.cleaned_data["name"]
                )
            )

        document.data = data
        # document.current_edit_meta.end_datetime = timezone.now()
        # document.current_edit_meta.closed = True
        # document.current_edit_meta.save()
        document.save()

        messages.success(request, "Successfully uploaded")
        return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def write_remark(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)
    reject_remark_id = request.GET.get("reject_remark_id")
    remark_to_reject = None

    try:
        reject_remark_id = int(reject_remark_id)
    except ValueError:
        raise Http404()

    if reject_remark_id is not None:
        remark_to_reject = get_object_or_404(Remark, id=reject_remark_id)

        if remark_to_reject.is_rejected:
            raise PermissionDenied()

    if document.current_edit_meta is None:
        raise PermissionDenied()

    form = RemarkForm(request.POST)

    context = browser_base_context(request)
    context.update({
        "form_title": "Write remark",
        "form": form,
        "submit_title": "Submit",
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

        messages.success(request, "Successfully submitted remark")
        return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def rename_document(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)
    old_name = document.name

    if request.method == "POST":
        form = RenameDocument(request.POST, instance=document.data)
    else:
        form = RenameDocument(instance=document.data)

    context = browser_base_context(request)
    context.update({
        "form_title": "Rename document",
        "form": form,
        "submit_title": "Rename",
        "validator_url": reverse("documents:validator-rename-document"),
    })

    if request.method == "POST" and form.is_valid():
        redirect_next = request.GET.get("next", "single")

        if old_name != form.cleaned_data["name"]:
            Activity.objects.create_for_document(
                request.user,
                document,
                user=request.user,
                content_type=Document.content_type,
                target_id=document.pk,
                details=strings.ACTIVITY_RENAME_DOCUMENT.format(
                    old_name=old_name,
                    new_name=form.cleaned_data["name"]
                )
            )

        form.save()
        messages.success(request, "Successfully renamed")

        if redirect_next == "list":
            return redirect(document.parent.permalink)
        else:
            return redirect(document.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)


@require_http_methods(["GET", "POST"])
@transaction.atomic
def rename_folder(request, name, path=None):
    parent_folder = get_folder_or_404(path)
    folder = get_object_or_404(Folder, parent=parent_folder, name=name)
    old_name = folder.name

    if request.method == "POST":
        form = RenameFolder(request.POST, instance=folder)
    else:
        form = RenameDocument(instance=folder)

    context = browser_base_context(request)
    context.update({
        "form_title": "Rename folder",
        "form": form,
        "submit_title": "Rename",
        "validator_url": reverse("documents:validator-rename-folder"),
    })

    if request.method == "POST" and form.is_valid():
        redirect_next = request.GET.get("next", "list")

        if old_name != form.cleaned_data["name"]:
            Activity.objects.create(
                user=request.user,
                content_type=Folder.content_type,
                target_id=folder.pk,
                details=strings.ACTIVITY_RENAME_FOLDER.format(
                    old_name=old_name,
                    new_name=form.cleaned_data["name"]
                )
            )

        form.save()
        messages.success(request, "Successfully renamed")

        if redirect_next == "list":
            return redirect(folder.parent.permalink)
        else:
            return redirect(folder.permalink)

    return TemplateResponse(template="forms/form.html", request=request, context=context)
