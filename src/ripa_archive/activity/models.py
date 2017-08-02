from django.db import models

from ripa_archive.accounts.models import User
from ripa_archive.documents.models import DocumentEditMeta, Remark, DocumentData


class Activity(models.Model):
    class Meta:
        ordering = ["-datetime"]

    user = models.ForeignKey(User)
    content_type = models.CharField(max_length=100, blank=True)
    document_data = models.ForeignKey(DocumentData, null=True)
    target_id = models.PositiveIntegerField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    details = models.TextField()


# class Notification(models.Model):
#     to = models.ForeignKey(User)
#     text = models.TextField()
#     content_type = models.CharField(max_length=100, blank=True)
#     target_id = models.PositiveIntegerField(null=True)
#     remark = models.ForeignKey(Remark, null=True)
