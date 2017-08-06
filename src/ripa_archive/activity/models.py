from django.db import models

from ripa_archive.accounts.models import User
from ripa_archive.documents.models import DocumentEditMeta, Remark, DocumentData, Document
from ripa_archive.notifications.models import Notification


class ActivityManager(models.Manager):
    def create(self, **kwargs):
        raise AssertionError("Use activity_factory instead")

    def bulk_create(self, objs, batch_size=None):
        raise AssertionError("Use activity_factory instead")


class Activity(models.Model):
    class Meta:
        ordering = ["-datetime"]

    user = models.ForeignKey(User)
    content_type = models.CharField(max_length=100, blank=True)
    document_data = models.ForeignKey(DocumentData, null=True)
    document_edit_meta = models.ForeignKey(DocumentEditMeta, null=True)
    target_id = models.PositiveIntegerField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    objects = ActivityManager()
    _factory_objects = models.Manager()
