from django.db import models

from ripa_archive.accounts.models import User


class PermissionManager(models.Manager):
    def for_folders(self):
        return self.all().filter(code__startswith="folders")

    def for_documents(self):
        return self.all().filter(code__startswith="documents")


class Permission(models.Model):
    code = models.CharField(max_length=60, unique=True)
    objects = PermissionManager()

    def __str__(self):
        return self.translations.get(language_code="ru").name


class PermissionTranslation(models.Model):
    class Meta:
        default_related_name = "translations"

    permission = models.ForeignKey(Permission)
    language_code = models.CharField(max_length=4)
    name = models.CharField(max_length=60)


class Group(models.Model):
    name = models.CharField(max_length=60)
    permissions = models.ManyToManyField(Permission)
    inherit = models.ManyToManyField('Group')

    def __str__(self):
        return self.name


class ModelWhichHaveCustomPermissionsMixin:
    custom_permission_model = None

    def is_user_has_permission(self, user, permission_name):
        return False


class PermissionModel(models.Model):
    class Meta:
        abstract = True

    users = models.ManyToManyField(User)
    groups = models.ManyToManyField(Group)


class ModelCustomPermission(models.Model):
    class Meta:
        abstract = True

    # for_instance = models.ForeignKey("SomeModel")
    groups = models.ManyToManyField(Group, blank=True)
    users = models.ManyToManyField(User, blank=True)
    permissions = models.ManyToManyField(Permission)
