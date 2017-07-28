from rest_framework import serializers

from ripa_archive.permissions.models import Group


class BulkInputSerializer(serializers.Serializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )
