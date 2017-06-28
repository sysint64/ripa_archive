from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ripa_archive.documents.views.input_serializers import BulkInputSerializer, \
    ChangeFolderInputSerializer


@api_view(["POST"])
def copy(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def cut(request):
    serializer = BulkInputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def paste(request):
    pass


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
