from autoslug import AutoSlugField
from django.db import models

from django.utils.translation import ugettext as _


class FolderManager(models.Manager):
    def get_by_path(self, path):
        parent_folder = self.filter(name="Root", parent=None).first()

        if path is None:
            return parent_folder

        folders_names = path.split("/")

        for folder_name in folders_names:
            parent_folder = self.filter(name=folder_name, parent=parent_folder).first()

            if parent_folder is None:
                return None

        return parent_folder


# Default folders: root and none
class Folder(models.Model):
    class Meta:
        default_related_name = "folders"

    parent = models.ForeignKey('Folder', null=True, blank=True)
    name = models.CharField(max_length=60)
    objects = FolderManager()

    @property
    def path(self):
        if self.parent is None and self.name == "Root":
            return "/"

        folders = [self.name]
        current_folder = self.parent

        while current_folder is not None:
            folders = [current_folder.name] + folders
            current_folder = current_folder.parent

            if current_folder is not None:
                if current_folder.parent is None and current_folder.name == "Root":
                    break

        return "/%s/" % "/".join(folders)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=20)
    allow_delete = models.BooleanField()

    def __str__(self):
        return self.name


class Document(models.Model):
    class Meta:
        default_related_name = "documents"

    folder = models.ForeignKey(Folder, null=True)

    @property
    def document_data(self):
        return DocumentData.objects.filter(document=self).order_by("-datetime").last()

    def __str__(self):
        if self.document_data is not None:
            return self.document_data.name

        return "None"


class DocumentType:
    TXT = "0"
    DOC = "1"
    PDF = "2"


class DocumentData(models.Model):
    document = models.ForeignKey(Document)
    status = models.ForeignKey(Status)
    file = models.FileField(upload_to="documents/")
    name = models.CharField(max_length=60)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def type(self):
        return DocumentType.TXT
