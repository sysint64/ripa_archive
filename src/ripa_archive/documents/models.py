import os

from django.db import models
from django.urls import reverse

from ripa_archive.accounts.models import User
from ripa_archive.permissions.models_abstract import ModelCustomPermission, ModelWhichHaveCustomPermissionsMixin


class FoldersManager(models.Manager):
    ALREADY_EXIST_ERROR = 'Folder with name "%s" already exist in this folder'

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

    def exist_with_name(self, name):
        return self.get_queryset().filter(name__iexact=name).count() > 0

    def for_user(self, user, folder=None):
        queryset = self.get_queryset()

        if user is None or user.group is None:
            return queryset.none()

        if folder is not None:
            if not folder.is_user_has_permission(user, "folders_can_read"):
                return queryset.none()

            return queryset.filter(parent=folder)
        else:
            if not user.group.has_permission("folders_can_read"):
                return queryset.none()

        return queryset


class DocumentsManager(models.Manager):
    ALREADY_EXIST_ERROR = 'Document with name "%s" already exist in this folder'

    def exist_with_name(self, name):
        for item in self.get_queryset().all():
            if item.data.name.lower() == name.lower():
                return True

        return False

    def for_user(self, user):
        queryset = self.get_queryset()
        return queryset


class FolderCustomPermission(ModelCustomPermission):
    for_instances = models.ManyToManyField("Folder")  # TODO: change to FK, cascade delete


class DocumentCustomPermission(ModelCustomPermission):
    for_instances = models.ManyToManyField("Document")  # TODO: change to FK, cascade delete


# Default folders: root and none
class Folder(ModelWhichHaveCustomPermissionsMixin, models.Model):
    class Meta:
        default_related_name = "folders"

    content_type = "documents.Folder"

    custom_permission_model = FolderCustomPermission
    parent = models.ForeignKey('Folder', null=True, blank=True)
    name = models.CharField(verbose_name="name", help_text="this is a help text", max_length=60)
    objects = FoldersManager()

    @property
    def permalink(self):
        if self.path != "":
            return reverse("documents:index", kwargs={"path": self.path})
        else:
            return reverse("documents:index")

    @property
    def path_folders(self):
        items = [self]
        current_folder = self.parent

        while current_folder is not None:
            items = [current_folder] + items
            current_folder = current_folder.parent
            print(current_folder)

        return items

    @property
    def path(self):
        folders = self.path_folders

        # Remove root folder
        if len(folders) >= 1 and folders[0].parent is None and folders[0].name == "Root":
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


class Document(models.Model):
    class Meta:
        default_related_name = "documents"

    content_type = "documents.Document"

    owner = models.ForeignKey(User, null=True, related_name="owner")
    contributors = models.ManyToManyField(User, related_name="contributors")
    followers = models.ManyToManyField(User, related_name="followers")

    data = models.OneToOneField("DocumentData", null=True, default=None)
    current_edit_meta = models.ForeignKey("DocumentEditMeta", null=True, default=None)
    parent = models.ForeignKey(Folder)
    status = models.ForeignKey(Status)

    objects = DocumentsManager()

    def _reverse(self, urlname, kwargs=None):
        if self.data is None:
            return ""

        if kwargs is None:
            kwargs = {}

        if self.parent.path != "":
            kwargs.update({"path": self.parent.path, "name": self.data.name})
        else:
            kwargs.update({"name": self.data.name})

        return reverse("documents:" + urlname, kwargs=kwargs)

    @property
    def permalink(self):
        return self._reverse("document")

    @property
    def last_version_file_permalink(self):
        return self._reverse("last-version-file")

    @property
    def upload_new_version_permalink(self):
        return self._reverse("upload-new-version")

    def data_permalink(self, data):
        return self._reverse("get-file", kwargs={"version": data.pk})

    @property
    def name(self):
        return self.data.name

    @property
    def last_data(self):
        return DocumentData.objects.filter(document=self).order_by("-datetime").last()

    @property
    def path(self):
        if self.parent.path != "":
            return self.parent.path + "/" + self.name
        else:
            return self.name

    @property
    def is_under_edition(self):
        return self.current_edit_meta is not None

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
    class Meta:
        default_related_name = "document_data_set"

    document = models.ForeignKey(Document)
    file = models.FileField(upload_to="documents/")
    name = models.CharField(max_length=60)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def filename(self):
        return self.file.name.split("/")[-1]

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

    @property
    def permalink(self):
        return self.document.data_permalink(self)


class DocumentEditMeta(models.Model):
    editor = models.ForeignKey(User)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True, default=None)
    document = models.ForeignKey(Document)
    closed = models.BooleanField(default=False)


class Remark(models.Model):
    class Status:
        ACTIVE = '0'
        ACCEPTED = '1'
        REJECTED = '2'
        FINISHED = '3'

        CHOICES = (
            (ACTIVE, "Active"),
            (ACCEPTED, "Accepted"),
            (REJECTED, "Rejected"),
            (FINISHED, "Finished"),
        )

    class Meta:
        ordering = ["-datetime"]

    edit_meta = models.ForeignKey(DocumentEditMeta)
    user = models.ForeignKey(User)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=Status.CHOICES, default=Status.ACTIVE)

    @property
    def is_accepted(self):
        return self.status == Remark.Status.ACCEPTED

    @property
    def is_rejected(self):
        return self.status == Remark.Status.REJECTED

    @property
    def is_finished(self):
        return self.status == Remark.Status.FINISHED

    @property
    def css_class(self):
        return {
            Remark.Status.ACCEPTED: " accepted",
            Remark.Status.REJECTED: " rejected",
            Remark.Status.FINISHED: " finished",
        }.get(self.status, "")
