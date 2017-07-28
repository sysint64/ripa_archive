from rest_framework import serializers

from ripa_archive.accounts.models import User


class BulkInputSerializer(serializers.Serializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=True
    )
