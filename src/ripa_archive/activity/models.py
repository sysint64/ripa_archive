from django.db import models

from ripa_archive.accounts.models import User
from ripa_archive.documents.models import DocumentEditMeta, Remark, DocumentData, Document, Folder
from ripa_archive.middleware import LanguageMiddleware
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
    ref_id = models.PositiveIntegerField(null=True)
    ref_content_type = models.CharField(blank=True, max_length=100)

    objects = ActivityManager()
    _factory_objects = models.Manager()

    @property
    def ref_text(self):
        translation = self.translations.filter(language_code=LanguageMiddleware.code).first()

        if translation is None:
            return ""

        return translation.ref_text

    @property
    def details(self):
        translation = self.translations.filter(language_code=LanguageMiddleware.code).first()

        if translation is None:
            return ""

        return translation.details

    @property
    def target_instance(self):
        if self.content_type == Document.content_type:
            return Document.objects.filter(id=self.target_id).first()

        elif self.content_type == Folder.content_type:
            return Folder.objects.filter(id=self.target_id).first()

    @property
    def permalink(self):
        instance = self.target_instance

        if instance is None:
            return ""

        return instance.permalink

    @property
    def ref_instance(self):
        cls = {
            Document.content_type: Document,
            Folder.content_type: Folder
        }.get(self.content_type)

        return cls.objects.filter(pk=self.ref_id).first()

    def __str__(self):
        if self.target_instance is None:
            return ""
        else:
            return str(self.target_instance)


class ActivityTranslation(models.Model):
    class Meta:
        default_related_name = "translations"

    activity = models.ForeignKey(Activity)
    language_code = models.CharField(max_length=4)
    ref_text = models.CharField(blank=True, max_length=100)
    details = models.TextField(default="")
