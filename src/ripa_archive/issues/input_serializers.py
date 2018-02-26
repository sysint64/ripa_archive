from rest_framework import serializers

from ripa_archive.issues.models import Issue


class BulkInputSerializer(serializers.Serializer):
    issues = serializers.PrimaryKeyRelatedField(
        queryset=Issue.objects.all(),
        many=True,
        required=True
    )
