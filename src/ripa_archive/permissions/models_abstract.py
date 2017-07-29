from django.db import models

from ripa_archive.accounts.models import User
from ripa_archive.permissions.models import Group, Permission


class ModelWhichHaveCustomPermissionsMixin:
    custom_permission_model = None

    def is_user_has_permission(self, user, permission):
        custom_permissions = self.custom_permission_model.objects.filter(for_instances=self)

        for custom_permission in custom_permissions:
            if user in custom_permission.users.all():
                return custom_permission.has_permission(permission)

            if user.group in custom_permission.groups.all():
                return custom_permission.has_permission(permission)

        return user.group.has_permission("folders_can_read")


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

    def has_permission(self, permission):
        return self.permissions.filter(code=permission).count() > 0