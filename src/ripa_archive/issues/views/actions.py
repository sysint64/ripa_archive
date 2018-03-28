from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ripa_archive.issues.input_serializers import BulkInputSerializer
from ripa_archive.issues.models import IssueItem, Issue


@api_view(["POST"])
def delete(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    issues = serializer.validated_data["issues"]

    with transaction.atomic():
        for issue in issues:
            issue.delete()

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
# TODO: @require_permissions
def start_working_on_item(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue_item = get_object_or_404(IssueItem, pk=request.data.get("id"), issue=issue)

    if issue.owner != request.user:
        raise PermissionError()

    issue_item.status = IssueItem.Status.IN_PROGRESS
    issue_item.save()
    messages.success(request._request, _("Successfully started working on issue item"))
    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
# TODO: @require_permissions
def pause_working_on_item(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue_item = get_object_or_404(IssueItem, pk=request.data.get("id"), issue=issue)

    is_user_superior_in_hierarchy = issue.owner.is_child_of(request.user)
    is_owner = request.user == issue.owner

    if not is_owner and not is_user_superior_in_hierarchy:
        raise PermissionError()

    issue_item.status = IssueItem.Status.PAUSED
    issue_item.save()
    messages.success(request._request, _("Successfully started working on issue item"))
    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
# TODO: @require_permissions
def confirm_item(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue_item = get_object_or_404(IssueItem, pk=request.data.get("id"), issue=issue)

    is_user_superior_in_hierarchy = issue.owner.is_child_of(request.user)

    if not is_user_superior_in_hierarchy:
        raise PermissionError()

    issue_item.status = IssueItem.Status.CONFIRMED
    issue_item.save()
    messages.success(request._request, _("Successfully started working on issue item"))
    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
# TODO: @require_permissions
def finish_working_on_item(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue_item = get_object_or_404(IssueItem, pk=request.data.get("id"), issue=issue)

    is_user_superior_in_hierarchy = issue.owner.is_child_of(request.user)
    is_owner = request.user == issue.owner

    if not is_owner and not is_user_superior_in_hierarchy:
        raise PermissionError()

    issue_item.status = IssueItem.Status.FINISHED
    issue_item.save()
    messages.success(request._request, _("Successfully finished working on issue item"))
    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
# TODO: @require_permissions
def approve_working_on_item(request, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    issue_item = get_object_or_404(IssueItem, pk=request.data.get("id"), issue=issue)

    if not issue.owner.is_child_of(request.user):
        raise PermissionError()

    issue_item.status = IssueItem.Status.APPROVED
    issue_item.save()
    messages.success(request._request, _("Successfully approved issue item"))
    return Response({}, status=status.HTTP_200_OK)
