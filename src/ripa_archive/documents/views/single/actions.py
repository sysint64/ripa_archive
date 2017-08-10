from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from request_helper import get_request_int_or_404
from ripa_archive.activity import activity_factory
from ripa_archive.activity.models import Activity
from ripa_archive.documents import strings
from ripa_archive.documents.models import Document, DocumentEditMeta, Remark
from ripa_archive.documents.views.main import get_folder_or_404
from ripa_archive.documents.views.single.main import get_document
from ripa_archive.notifications.models import Notification
from ripa_archive.notifications import notifications_factory
from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import require_permissions


@api_view(["POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_TAKE_DOCUMENT_FOR_REVISION], get_instance_functor=get_document)
def take_for_revision(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.is_under_edition:
        raise ValidationError("Already under edition")

    # Attach editor to document
    edit_meta = DocumentEditMeta.objects.create(
        editor=request.user,
        document=document,
        previous_document_data=document.data
    )

    document.current_edit_meta = edit_meta
    document.save()

    messages.success(request._request, "Successfully took")
    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_READ], get_instance_functor=get_document)
def toggle_follow(request, name, path=None):
    document = get_document(name=name, path=path)

    if request.user in document.followers.all():
        document.followers.remove(request.user)
    else:
        document.followers.add(request.user)

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_REVIEW], get_instance_functor=get_document)
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
@require_permissions([codes.DOCUMENTS_CAN_TAKE_DOCUMENT_FOR_REVISION], get_instance_functor=get_document)
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
@require_permissions([codes.DOCUMENTS_CAN_REVERT], get_instance_functor=get_document)
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

    activity_factory.for_document(
        request.user,
        document,
        strings.ACTIVITY_REVERT_DOCUMENT.format(datetime=activity.datetime),
        document_data=activity.document_data
    )

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_REVIEW], get_instance_functor=get_document)
def accept_document(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.current_edit_meta is None:
        raise PermissionDenied()

    notifications_factory.notification_document(
        request.user,
        document,
        strings.NOTIFICATION_DOCUMENT_ACCEPTED
    )

    edit_meta = document.current_edit_meta
    edit_meta.end_datetime = timezone.now()
    edit_meta.status = DocumentEditMeta.Status.ACCEPTED
    edit_meta.closed_by = request.user
    edit_meta.save()

    document.accepted_edit_meta = document.current_edit_meta
    document.current_edit_meta = None
    document.save()

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
@require_permissions([codes.DOCUMENTS_CAN_REVIEW], get_instance_functor=get_document)
def reject_document(request, name, path=None):
    document = get_document(name=name, path=path)

    if document.current_edit_meta is None:
        raise PermissionDenied()

    notifications_factory.notification_document(
        request.user,
        document,
        strings.NOTIFICATION_DOCUMENT_REJECTED
    )

    edit_meta = document.current_edit_meta
    edit_meta.end_datetime = timezone.now()
    edit_meta.status = DocumentEditMeta.Status.REJECTED
    edit_meta.closed_by = request.user
    edit_meta.save()

    document.accepted_edit_meta = document.current_edit_meta
    document.current_edit_meta = None
    document.data = edit_meta.previous_document_data
    document.save()

    activity_factory.for_document(
        request.user,
        document,
        strings.ACTIVITY_REVERT_DOCUMENT.format(
            datetime=edit_meta.previous_document_data.datetime
        ),
        document_data=edit_meta.previous_document_data
    )

    return Response({}, status=status.HTTP_200_OK)
