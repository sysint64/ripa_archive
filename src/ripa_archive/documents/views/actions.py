from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ripa_archive.documents.models import Folder, Document
from ripa_archive.documents.views.input_serializers import BulkInputSerializer, \
    ChangeFolderInputSerializer
from ripa_archive.documents.views.main import get_folder_or_404


@api_view(["POST"])
def copy(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    folders = serializer.validated_data["folders"]
    documents = serializer.validated_data["documents"]

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
                new_src_folder_id = item.id
                item.pk = None
                item.parent = dst_folder
                item.save()

                if isinstance(item, Folder):
                    copy_content(dst_folder=item, src_folder_id=new_src_folder_id)

        _copy(Folder.objects.filter(parent__id=src_folder_id))
        _copy(Document.objects.filter(parent__id=src_folder_id))

    # TODO: add copy action to log
    def copy_document_data(dst_document, src_document_id):
        src_document = Document.objects.filter(pk=src_document_id).first()

        for document_data in src_document.document_data_set.all():
            document_data.pk = None
            document_data.document = dst_document
            document_data.save()

    def do_paste(items, manager, to_folder_manager):
        for item_id in items:
            item = manager.filter(id=item_id).first()

            if item is None:
                continue

            if to_folder_manager.exist_with_name(item.name):
                raise ValidationError(to_folder_manager.ALREADY_EXIST_ERROR % item.name)

            item.parent = to_folder

            if do_cut:
                item.save()
            else:  # make copy
                item.pk = None
                item.save()

                if isinstance(item, Folder):
                    copy_content(dst_folder=item, src_folder_id=item_id)
                elif isinstance(item, Document):
                    copy_document_data(dst_document=item, src_document_id=item_id)

    with transaction.atomic():
        do_paste(folders, Folder.objects, to_folder.folders)
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

    folders = serializer.validated_data["folders"]
    documents = serializer.validated_data["documents"]

    def delete_all(items):
        for item in items:
            item.delete()

    with transaction.atomic():
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
            if manager.exist_with_name(item.name):
                raise ValidationError(manager.ALREADY_EXIST_ERROR % item.name)

            item.parent = to_folder
            item.save()

    with transaction.atomic():
        update_parent(folders, to_folder.folders)
        update_parent(documents, to_folder.documents)

    return Response({}, status=status.HTTP_200_OK)
