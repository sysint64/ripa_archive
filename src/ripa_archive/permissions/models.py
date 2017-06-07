from django.db import models

from ripa_archive.accounts.models import User


class Permission(models.Model):
    name = models.CharField(max_length=60)
    strict_name = models.CharField(max_length=60)
    code = models.CharField(max_length=60)


class Group(models.Model):
    name = models.CharField(max_length=60)
    permissions = models.ManyToManyField(Permission)
    inherit = models.ManyToManyField('Group')


class ModelWhichHaveStrictsMixin:
    strict_model = None

    def is_user_has_permission(self, user, permission_name):
        return False


class PermissionModel(models.Model):
    class Meta:
        abstract = True

    users = models.ManyToManyField(User)
    groups = models.ManyToManyField(Group)


class ModelStrict(models.Model):
    class Meta:
        abstract = True

    # for_instance = models.ForeignKey("SomeModel")
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=60)
    groups = models.ManyToManyField(Group)
    users = models.ManyToManyField(User)
    custom_permissions = models.ManyToManyField(Permission)
