import os

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from ripa_archive.permissions.models import ModelHavePermissionsMixin


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
    name = models.CharField(verbose_name="name", help_text="this is a help text", max_length=60)
    objects = FolderManager()

    @property
    def permalink(self):
        if self.path != "":
            return reverse("documents:browser", kwargs={"path": self.path})
        else:
            return reverse("documents:browser")

    @property
    def path_folders(self):
        items = [self]
        current_folder = self.parent

        while current_folder is not None:
            items = [current_folder] + items
            current_folder = current_folder.parent

        return items

    @property
    def path(self):
        folders = self.path_folders

        # Remove root folder
        if len(folders) >= 1 and folders[0].parent == None and folders[0].name == "Root":
            folders = folders[1:]

        return "/".join([str(folder) for folder in folders])

    @property
    def breadcrumbs(self):
        items = []

        for folder in self.path_folders:
            items.append({"name": folder.name, "permalink": folder.permalink})

        return items

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=20)
    allow_delete = models.BooleanField()

    def __str__(self):
        return self.name


class Document(ModelHavePermissionsMixin, models.Model):
    class Meta:
        default_related_name = "documents"

    owner = models.ForeignKey(User, null=True, related_name="owner")
    contributors = models.ManyToManyField(User, related_name="contributors")

    folder = models.ForeignKey(Folder, null=True)  # TODO: rm null=True
    status = models.ForeignKey(Status, null=True)  # TODO: rm null=True

    @property
    def data(self):
        return DocumentData.objects.filter(document=self).order_by("-datetime").last()

    def __str__(self):
        if self.data is not None:
            return self.data.name

        return "None"


class DocumentType:
    FILE = "0"
    TEXT = "1"
    WORD = "2"
    PDF = "3"
    SOUND = "4"
    EXCEL = "5"
    ARCHIVE = "6"
    IMAGE = "7"
    VIDEO = "8"
    POWERPOINT = "9"

    EXTENSIONS = (
        (TEXT, ("txt",)),
        (PDF, ("pdf",)),
        (SOUND, ("mp3", "wav", "flac", "acc",)),
        (ARCHIVE, ("7z", "zip", "rar", "tar", "gz",)),
        (IMAGE, ("jpg", "jpeg", "png",)),
        (VIDEO, ("avi", "mp4", "mpeg4", "3gp",)),
        (WORD, ("doc", "docx",)),
        (EXCEL, ("xls", "xlsx", "xlsb",)),
        (POWERPOINT, ("ppt", "pptx",)),
    )

    @staticmethod
    def get_type_from_name(name):
        _, ext = os.path.splitext(name)
        ext = ext[1:]

        for type_extensions_pair in DocumentType.EXTENSIONS:
            document_type, extensions = type_extensions_pair

            if ext in extensions:
                return document_type

        return DocumentType.FILE


class DocumentData(models.Model):
    document = models.ForeignKey(Document)
    file = models.FileField(upload_to="documents/")
    name = models.CharField(max_length=60)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def type(self):
        return DocumentType.get_type_from_name(self.file.name)

    @property
    def icon(self):
        return {
            DocumentType.FILE: "fa-file-o",
            DocumentType.EXCEL: "fa-file-excel-o",
            DocumentType.PDF: "fa-file-pdf-o",
            DocumentType.SOUND: "fa-file-sound-o",
            DocumentType.TEXT: "fa-file-text-o",
            DocumentType.ARCHIVE: "fa-file-archive-o",
            DocumentType.WORD: "fa-file-word-o",
            DocumentType.IMAGE: "fa-file-image-o",
            DocumentType.VIDEO: "fa-file-video-o",
            DocumentType.POWERPOINT: "fa-file-powerpoint-o",
        }.get(self.type, "fa-file-o")
