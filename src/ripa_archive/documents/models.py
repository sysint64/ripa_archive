import os

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ripa_archive.accounts.models import User
from ripa_archive.documents.validators import NAME_MAX_LENGTH
from ripa_archive.permissions import codes
from ripa_archive.permissions.models_abstract import ModelCustomPermission, ModelWhichHaveCustomPermissionsMixin


class FoldersManager(models.Manager):
    ALREADY_EXIST_ERROR = _('Folder with name "%s" already exist in this folder')

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

    def exist_with_name(self, parent, name, instance=None):
        qs = self.get_queryset().filter(parent=parent, name__iexact=name)

        if instance is not None:
            qs = qs.exclude(pk=instance.pk)

        return qs.count() > 0

    def for_user(self, user, folder=None):
        queryset = self.get_queryset()

        if user is None or user.group is None:
            return queryset.none()

        if folder is not None:
            if not folder.is_user_has_permission(user, codes.FOLDERS_CAN_READ):
                return queryset.none()

            return queryset.filter(parent=folder)
        else:
            if not user.group.has_permission(codes.FOLDERS_CAN_READ):
                return queryset.none()

        return queryset


class DocumentsManager(models.Manager):
    ALREADY_EXIST_ERROR = _('Document with name "%s" already exist in this folder')

    def exist_with_name(self, parent, name, instance=None):
        qs = self.get_queryset().filter(parent=parent, name__iexact=name)

        if instance is not None:
            qs = qs.exclude(pk=instance.pk)

        return qs.count() > 0

    def for_user(self, user, folder=None):
        queryset = self.get_queryset()

        if user is None or user.group is None:
            return queryset.none()

        if folder is not None:
            if not folder.is_user_has_permission(user, codes.DOCUMENTS_CAN_READ):
                return queryset.none()

            return queryset.filter(parent=folder)
        else:
            if not user.group.has_permission(codes.DOCUMENTS_CAN_READ):
                return queryset.none()

        return queryset


class FolderCustomPermission(ModelCustomPermission):
    for_instance = models.ForeignKey("Folder")


class DocumentCustomPermission(ModelCustomPermission):
    for_instance = models.ForeignKey("Document")


# Default folders: root and none
class Folder(ModelWhichHaveCustomPermissionsMixin, models.Model):
    class Meta:
        default_related_name = "folders"

    content_type = "documents.Folder"

    custom_permission_model = FolderCustomPermission
    parent = models.ForeignKey('Folder', null=True, blank=True)
    name = models.CharField(verbose_name=_("Name"), max_length=NAME_MAX_LENGTH)
    objects = FoldersManager()

    @property
    def permalink(self):
        if self.path != "":
            return reverse("documents:index", kwargs={"path": self.path})
        else:
            return reverse("documents:index")

    @property
    def archive_permalink(self):
        if self.path != "":
            return reverse("documents:archive", kwargs={"path": self.path})
        else:
            return reverse("documents:archive")

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

    @property
    def archive_breadcrumbs(self):
        items = []

        for folder in self.path_folders:
            items.append({"name": folder.name, "permalink": folder.archive_permalink})

        return items

    def __str__(self):
        return self.name


class Document(ModelWhichHaveCustomPermissionsMixin, models.Model):
    class Meta:
        default_related_name = "documents"

    class Status:
        OPEN = "0"
        IN_PROGRESS = "1"
        PROJECT = "2"
        FINAL = "3"
        CLOSE = "4"

        FORM_CHOICES = (
            (OPEN, _("Open")),
            # (IN_PROGRESS, "In progress"),
            (PROJECT, _("Project")),
            (FINAL, _("Final")),
            (CLOSE, _("Close")),
        )

        ALL_CHOICES = (
            (OPEN, _("Open")),
            (IN_PROGRESS, _("In progress")),
            (PROJECT, _("Project")),
            (FINAL, _("Final")),
            (CLOSE, _("Close")),
        )

    content_type = "documents.Document"
    custom_permission_model = DocumentCustomPermission

    name = models.CharField(max_length=NAME_MAX_LENGTH, default="No name")
    owner = models.ForeignKey(User, null=True, related_name="owner")
    contributors = models.ManyToManyField(User, related_name="contributors")
    followers = models.ManyToManyField(User, related_name="followers")

    data = models.OneToOneField("DocumentData", null=True, default=None)
    current_edit_meta = models.ForeignKey("DocumentEditMeta", null=True, default=None)
    accepted_edit_meta = models.ForeignKey("DocumentEditMeta", null=True, default=None, related_name="accepted_edit_meta")
    parent = models.ForeignKey(Folder)
    status = models.CharField(verbose_name=_("Status"), max_length=2, default=Status.OPEN, choices=Status.FORM_CHOICES)

    objects = DocumentsManager()

    def _reverse(self, urlname, kwargs=None):
        if self.data is None:
            return ""

        if kwargs is None:
            kwargs = {}

        if self.parent.path != "":
            kwargs.update({"path": self.parent.path, "name": self.name})
        else:
            kwargs.update({"name": self.name})

        return reverse("documents:" + urlname, kwargs=kwargs)

    @property
    def status_str(self):
        return dict(Document.Status.ALL_CHOICES).get(self.status, "Undefined")

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
        return self.name


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
    file = models.FileField(verbose_name=_("File"), upload_to="documents/")
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

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
    class Status:
        ACTIVE = '0'
        ACCEPTED = '1'
        REJECTED = '2'

    editor = models.ForeignKey(User)
    closed_by = models.ForeignKey(User, related_name="accepted_by", null=True)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(null=True, default=None)
    document = models.ForeignKey(Document)
    previous_document_data = models.ForeignKey(DocumentData, null=True)
    status = models.CharField(max_length=1, default=Status.ACTIVE)

    @property
    def is_accepted(self):
        return self.status == DocumentEditMeta.Status.ACCEPTED

    @property
    def is_rejected(self):
        return self.status == DocumentEditMeta.Status.REJECTED

    @property
    def is_active(self):
        return self.status == DocumentEditMeta.Status.ACTIVE

    @property
    def time_spent(self):
        return self.end_datetime - self.start_datetime

    @property
    def css_class(self):
        return {
            DocumentEditMeta.Status.ACCEPTED: " accepted",
            DocumentEditMeta.Status.REJECTED: " rejected",
        }.get(self.status, "")


class ActiveRemarkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(edit_meta__status=DocumentEditMeta.Status.ACTIVE)


class Remark(models.Model):
    class Status:
        ACTIVE = '0'
        ACCEPTED = '1'
        REJECTED = '2'
        FINISHED = '3'

    class Meta:
        ordering = ["-datetime"]

    edit_meta = models.ForeignKey(DocumentEditMeta)
    user = models.ForeignKey(User)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, default=Status.ACTIVE)

    objects = models.Manager()
    active_objects = ActiveRemarkManager()

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
    def is_active(self):
        return self.status == Remark.Status.ACTIVE

    @property
    def css_class(self):
        return {
            Remark.Status.ACCEPTED: " accepted",
            Remark.Status.REJECTED: " rejected",
            Remark.Status.FINISHED: " finished",
        }.get(self.status, "")
