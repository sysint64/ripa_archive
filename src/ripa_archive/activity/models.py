from django.db import models
from django.db import transaction

from ripa_archive.accounts.models import User
from ripa_archive.documents.models import DocumentEditMeta, Remark, DocumentData, Document
from ripa_archive.notifications.models import Notification


class ActivityManager(models.Manager):
    @transaction.atomic
    def create_for_document(self, sender, document, **kwargs):
        """
        Create activity for document and send notifications to followers
        """
        instance = self.create(**kwargs)
        assert instance.content_type == "documents.Document"

        for follower in document.followers.exclude(pk=sender.pk):
            Notification.objects.create(
                to=follower,
                user=sender,
                title=str(document),
                text=instance.details,
                content_type="documents.Document",
                target_id=document.id
            )

        return instance


class Activity(models.Model):
    class Meta:
        ordering = ["-datetime"]

    user = models.ForeignKey(User)
    content_type = models.CharField(max_length=100, blank=True)
    document_data = models.ForeignKey(DocumentData, null=True)
    target_id = models.PositiveIntegerField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    objects = ActivityManager()
