from django.contrib.auth.models import User
from django.db import models


class Permission(models.Model):
    parent = models.ForeignKey("Permission", null=True)
    name = models.CharField(max_length=60)


class Group(models.Model):
    name = models.CharField(max_length=60)
    permissions = models.ManyToManyField(Permission)


class ModelHavePermissionsMixin:
    def is_user_has_permission(self, user, permission_name):
        return False


class PermissionModel(models.Model):
    class Meta:
        abstract = True

    users = models.ManyToManyField(User)
    groups = models.ManyToManyField(Group)
