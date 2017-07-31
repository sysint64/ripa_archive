from rest_framework import serializers

from ripa_archive.documents.models import Folder, Document


class BulkInputSerializer(serializers.Serializer):
    folders = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(),
        many=True,
        required=False,
        default=[]
    )
    documents = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(),
        many=True,
        required=False,
        default=[]
    )


class ChangeFolderInputSerializer(BulkInputSerializer):
    to_folder = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(),
        required=True
    )
