from django.db import models

from ripa_archive.accounts.models import User
from ripa_archive.documents.models import Document, Folder


class Notification(models.Model):
    class Meta:
        ordering = ["-datetime"]

    to = models.ForeignKey(User, related_name="to_user")
    user = models.ForeignKey(User)
    text = models.TextField()
    detail = models.TextField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    target_id = models.PositiveIntegerField(null=True)
    is_read = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def permalink(self):
        cls = {
            Document.content_type: Document,
            Folder.content_type: Folder
        }.get(self.content_type)

        instance = cls.objects.filter(id=self.target_id).first()

        if instance is None:
            return ""

        return instance.permalink

