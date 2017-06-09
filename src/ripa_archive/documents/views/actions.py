from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.response import Response

from ripa_archive.documents.models import Folder
from ripa_archive.request_conv import string_to_integer_list


@require_http_methods(["POST"])
def copy(request):
    pass


@require_http_methods(["POST"])
def cut(request):
    pass


@require_http_methods(["POST"])
def paste(request):
    pass


@require_http_methods(["POST"])
def delete(request):
    pass


@api_view(["POST"])
def change_folder(request):
    class InputSerializer(serializers.Serializer):
        to_folder = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), required=True)
        folders = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), many=True, required=False)
        documents = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), many=True, required=False)

    serializer = InputSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    to_folder = serializer.validated_data["to_folder"]
    folders = serializer.validated_data["folders"]
    documents = serializer.validated_data["documents"]

    def update_parent(items):
        for item in items:
            item.parent = to_folder
            item.save()

    update_parent(folders)
    update_parent(documents)

    return Response({}, status=status.HTTP_200_OK)
