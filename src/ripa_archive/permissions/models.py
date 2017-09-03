from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from ripa_archive.middleware import LanguageMiddleware


class PermissionManager(models.Manager):
    def for_folders(self):
        return self.all().filter(code__startswith="folders")

    def for_documents(self):
        return self.all().filter(code__startswith="documents")

    def for_generic_folders(self):
        return self.all().filter(code__startswith="folders").exclude(code__contains="this")

    def for_generic_documents(self):
        return self.all().filter(code__startswith="documents").exclude(code__contains="this")

    def common(self):
        return self.all().filter(Q(code__startswith="activity") | Q(code__startswith="users") | Q(code__startswith="groups") | Q(code__startswith="statistics"))


class Permission(models.Model):
    code = models.CharField(max_length=255, unique=True)
    objects = PermissionManager()

    def __str__(self):
        return self.translations.get(language_code=LanguageMiddleware.code).name


class PermissionTranslation(models.Model):
    class Meta:
        default_related_name = "translations"

    permission = models.ForeignKey(Permission)
    language_code = models.CharField(max_length=4)
    name = models.CharField(max_length=255)


class Group(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    permissions = models.ManyToManyField(Permission)
    inherit = models.ManyToManyField('Group')

    def __str__(self):
        return self.name

    @property
    def ref(self):
        return self.name

    def has_permission(self, permission):
        if "this" in permission:
            return True

        has_perm = self.permissions.filter(code=permission).count() > 0

        for inherit_group in self.inherit.all():
            has_perm = has_perm or inherit_group.has_permission(permission)

        return has_perm
