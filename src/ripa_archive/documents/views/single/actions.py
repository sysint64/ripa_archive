from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from request_helper import get_request_int_or_404
from ripa_archive.activity.models import Activity
from ripa_archive.documents import strings
from ripa_archive.documents.models import Document, DocumentEditMeta, Remark
from ripa_archive.documents.views.main import get_folder_or_404
from ripa_archive.notifications.models import Notification
from ripa_archive.notifications import notifications_factory
from ripa_archive.permissions.decorators import require_permissions


def get_document(*args, **kwargs):
    path, name = kwargs.get("path"), kwargs["name"]
    parent_folder = get_folder_or_404(path)
    document = get_object_or_404(Document, parent=parent_folder, data__name=name)
    return document


@api_view(["POST"])
@transaction.atomic
@require_permissions(["documents_can_take_for_revision"], get_instance_functor=get_document)
def take_for_revision(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.is_under_edition:
        raise ValidationError("Already under edition")

    # Attach editor to document
    edit_meta = DocumentEditMeta.objects.create(editor=request.user, document=document)
    document.current_edit_meta = edit_meta
    document.save()

    messages.success(request._request, "Successfully took")
    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
@require_permissions(["documents_can_read"], get_instance_functor=get_document)
def toggle_follow(request, name, path=None):
    document = get_document(name=name, path=path)

    if request.user in document.followers.all():
        document.followers.remove(request.user)
    else:
        document.followers.add(request.user)

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def accept_remark(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.current_edit_meta is None:
        raise PermissionDenied()

    remark_id = get_request_int_or_404(request, "data", "remark_id")
    remark = get_object_or_404(Remark, id=remark_id)

    if remark.is_accepted:
        raise ValidationError({"details": "Already accepted"})

    remark.status = Remark.Status.ACCEPTED
    remark.save()

    # Send notification
    notifications_factory.notification_remark(
        request.user,
        document,
        remark,
        strings.NOTIFICATION_REMARK_ACCEPTED
    )

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def mark_as_finished_remark(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.current_edit_meta is None:
        raise PermissionDenied()

    remark_id = get_request_int_or_404(request, "data", "remark_id")
    remark = get_object_or_404(Remark, id=remark_id)

    remark.status = Remark.Status.FINISHED
    remark.save()

    # Send notification
    notifications_factory.notification_remark(
        request.user,
        document,
        remark,
        strings.NOTIFICATION_REMARK_FINISHED,
        to_followers=True
    )

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def revert_document(request, name, path=None):
    document = get_document(name=name, path=path)
    activity_id = get_request_int_or_404(request, "data", "activity_id")
    activity = get_object_or_404(Activity, id=activity_id)

    if activity.document_data is None:
        raise ValidationError("Activity does not provide data")

    if document.data.id == activity.document_data.id:
        raise ValidationError("Already this version")

    document.data = activity.document_data
    document.save()

    Activity.objects.create_for_document(
        request.user,
        document,
        user=request.user,
        content_type=Document.content_type,
        target_id=document.pk,
        document_data=activity.document_data,
        details=strings.ACTIVITY_REVERT_DOCUMENT.format(datetime=activity.datetime)
    )

    return Response({}, status=status.HTTP_200_OK)
