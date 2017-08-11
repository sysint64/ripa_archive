from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import PermissionDenied as RestPermissionDenied

from ripa_archive.permissions import codes
from ripa_archive.permissions.decorators import check_permissions


def check_bulk_permissions(request, folders, documents, folders_permissions, documents_permissions):
    try:
        for folder in folders:
            check_permissions(request, folders_permissions, folder)

        for document in documents:
            check_permissions(request, documents_permissions, document)
    except PermissionDenied:
        raise RestPermissionDenied()


def check_bulk_permissions_edit(request, folders, documents):
    check_bulk_permissions(
        request,
        folders,
        documents,
        [codes.FOLDERS_CAN_EDIT],
        [codes.DOCUMENTS_CAN_EDIT]
    )


def check_bulk_permissions_delete(request, folders, documents):
    check_bulk_permissions(
        request,
        folders,
        documents,
        [codes.FOLDERS_CAN_EDIT],
        [codes.DOCUMENTS_CAN_EDIT]
    )
