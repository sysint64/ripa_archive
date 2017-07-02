from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ripa_archive.documents.models import Folder
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
    parent_folder = get_folder_or_404(path)

    do_cut = request.session.get("cut_folders", []) != [] or \
             request.session.get("cut_documents", []) != []

    print(do_cut)

    folders = request.session.get("copied_folders", [])
    folders.extend(request.session.get("cut_folders", []))

    documents = request.session.get("copied_documents", [])
    documents.extend(request.session.get("cut_documents", []))

    with transaction.atomic():
        if do_cut:
            Folder.objects.filter(id__in=folders).update(parent=parent_folder)
        else:
            for folder_id in folders:
                folder = Folder.objects.filter(pk=folder_id).first()
                folder.pk = None
                folder.parent = parent_folder
                folder.save()

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
            if manager.filter(name=item.name).count() > 0:
                raise ValidationError(manager.ALREADY_EXIST_ERROR % item.name)

            item.parent = to_folder
            item.save()

    with transaction.atomic():
        update_parent(folders, to_folder.folders)
        update_parent(documents, to_folder.documents)

    return Response({}, status=status.HTTP_200_OK)
