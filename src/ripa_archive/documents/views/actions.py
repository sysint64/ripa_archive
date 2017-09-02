from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied as RestPermissionDenied
from rest_framework.response import Response

from ripa_archive.activity import activity_factory
from ripa_archive.documents import strings
from ripa_archive.documents.models import Folder, Document
from ripa_archive.documents.views.input_serializers import BulkInputSerializer, \
    ChangeFolderInputSerializer
from ripa_archive.documents.views.main import get_folder_or_404
from ripa_archive.documents.views.permissions import check_bulk_permissions_edit, \
    check_bulk_permissions_delete
from ripa_archive.permissions import codes


@api_view(["POST"])
def copy(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    folders = serializer.validated_data["folders"]
    documents = serializer.validated_data["documents"]

    with transaction.atomic():
        check_bulk_permissions_edit(request, folders, documents)

    request.session["copied_folders"] = [folder.id for folder in folders]
    request.session["copied_documents"] = [document.id for document in documents]

    request.session["cut_folders"] = []
    request.session["cut_documents"] = []

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
def cut(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    folders = serializer.validated_data["folders"]
    documents = serializer.validated_data["documents"]

    with transaction.atomic():
        check_bulk_permissions_edit(request, folders, documents)

    request.session["copied_folders"] = []
    request.session["copied_documents"] = []

    request.session["cut_folders"] = [folder.id for folder in folders]
    request.session["cut_documents"] = [document.id for document in documents]

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
def paste(request, path=None):
    to_folder = get_folder_or_404(path)

    do_cut = request.session.get("cut_folders", []) != [] or \
        request.session.get("cut_documents", []) != []

    folders = request.session.get("copied_folders", [])
    folders.extend(request.session.get("cut_folders", []))

    documents = request.session.get("copied_documents", [])
    documents.extend(request.session.get("cut_documents", []))

    def copy_content(dst_folder, src_folder_id):
        def _copy(manager):
            for item in manager.all():
                src_item_id = item.id
                item.pk = None
                item.parent = dst_folder

                activity_factory.for_folder(
                    request.user,
                    dst_folder,
                    strings.ACTIVITY_COPY_FOLDER,
                    ref={
                        "id": src_folder_id,
                        "content_type": Folder.content_type,
                        "text": "Source folder",
                    }
                )

                if isinstance(item, Document):
                    copy_document_data(dst_document=item, src_document_id=src_item_id)

                elif isinstance(item, Folder):
                    item.save()
                    copy_content(dst_folder=item, src_folder_id=src_item_id)

        _copy(Folder.objects.filter(parent__id=src_folder_id))
        _copy(Document.objects.filter(parent__id=src_folder_id))

    def copy_document_data(dst_document, src_document_id):
        src_document = Document.objects.filter(pk=src_document_id).first()

        data = dst_document.data
        data.pk = None
        data.save()

        dst_document.data = data
        dst_document.save()

        activity_factory.for_document(
            request.user,
            dst_document,
            strings.ACTIVITY_COPY_DOCUMENT,
            ref={
                "instance": src_document,
                "text": "Source document",
            }
        )

    def do_paste(items, manager, to_folder_manager):
        for item_id in items:
            item = manager.filter(id=item_id).first()

            if item is None:
                continue

            if to_folder_manager.exist_with_name(item.parent, item.name):
                raise ValidationError(to_folder_manager.ALREADY_EXIST_ERROR % item.name)

            old_path = item.path
            item.parent = to_folder

            if do_cut:
                item.save()

                if isinstance(item, Folder):
                    activity_factory.for_folder(
                        request.user,
                        item,
                        strings.ACTIVITY_MOVE_FOLDER.format(
                            old_path=old_path,
                            new_path=item.path
                        )
                    )
                elif isinstance(item, Document):
                    activity_factory.for_document(
                        request.user,
                        item,
                        strings.ACTIVITY_MOVE_DOCUMENT.format(
                            old_path=old_path,
                            new_path=item.path
                        )
                    )
                else:
                    raise SuspiciousOperation()

            else:  # make copy
                if isinstance(item, Folder):
                    item.pk = None
                    item.save()
                    copy_content(dst_folder=item, src_folder_id=item_id)
                elif isinstance(item, Document):
                    item.pk = None
                    copy_document_data(dst_document=item, src_document_id=item_id)

    with transaction.atomic():
        if len(folders) > 0:
            if not to_folder.is_user_has_permission(request.user, codes.FOLDERS_CAN_CREATE_FOLDERS_INSIDE_THIS_FOLDER):
                raise RestPermissionDenied()

            if not request.user.group.has_permission(codes.FOLDERS_CAN_CREATE):
                raise RestPermissionDenied()

            do_paste(folders, Folder.objects, to_folder.folders)

        if len(documents) > 0:

            if not to_folder.is_user_has_permission(request.user, codes.FOLDERS_CAN_CREATE_DOCUMENTS_INSIDE_THIS_FOLDER):
                raise RestPermissionDenied()

            if not request.user.group.has_permission(codes.DOCUMENTS_CAN_CREATE):
                raise RestPermissionDenied()

            do_paste(documents, Document.objects, to_folder.documents)

        request.session["copied_folders"] = []
        request.session["copied_documents"] = []
        request.session["cut_folders"] = []
        request.session["cut_documents"] = []

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
def delete(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    folders = serializer.validated_data.get("folders", [])
    documents = serializer.validated_data.get("documents", [])

    if len(folders) == 0 and len(documents) == 0:
        raise SuspiciousOperation("No selected items")

    def delete_all(items):
        for item in items:
            if isinstance(item, Folder):
                activity_factory.for_folder(
                    request.user,
                    item,
                    strings.ACTIVITY_DELETE_FOLDER.format(path=item.path)
                )
            elif isinstance(item, Document):
                activity_factory.for_document(
                    request.user,
                    item,
                    strings.ACTIVITY_DELETE_DOCUMENT.format(path=item.path)
                )
            else:
                raise SuspiciousOperation()

            item.delete()

    with transaction.atomic():
        check_bulk_permissions_delete(request, folders, documents)
        delete_all(folders)
        delete_all(documents)

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
def change_folder(request):
    serializer = ChangeFolderInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    to_folder = serializer.validated_data["to_folder"]
    folders = serializer.validated_data["folders"]
    documents = serializer.validated_data["documents"]

    def update_parent(items, manager):
        for item in items:
            if manager.exist_with_name(item.parent, item.name):
                raise ValidationError(manager.ALREADY_EXIST_ERROR % item.name)

            old_path = item.path
            item.parent = to_folder
            item.save()

            if isinstance(item, Folder):
                activity_factory.for_folder(
                    request.user,
                    item,
                    strings.ACTIVITY_MOVE_FOLDER.format(
                        old_path=old_path,
                        new_path=item.path
                    )
                )
            elif isinstance(item, Document):
                activity_factory.for_document(
                    request.user,
                    item,
                    strings.ACTIVITY_MOVE_DOCUMENT.format(
                        old_path=old_path,
                        new_path=item.path
                    )
                )
            else:
                raise SuspiciousOperation()

    with transaction.atomic():
        check_bulk_permissions_edit(request, folders, documents)
        update_parent(folders, to_folder.folders)
        update_parent(documents, to_folder.documents)

    return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
def sort_by(request):
    sort_by = request.data.get("sort_by")
    sort_direction = request.data.get("sort_direction")

    if sort_by not in ("name", "status", "datetime"):
        raise ValidationError("Bad sort field")

    if sort_direction not in ("asc", "desc"):
        raise ValidationError("Bad sort direction")

    request.session["documents-sort-by"] = "%s,%s" % (sort_by, sort_direction)
    return Response({}, status=status.HTTP_200_OK)
