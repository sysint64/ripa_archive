# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-10 13:02
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    PermissionTranslation = apps.get_model("permissions", "PermissionTranslation")

    # Create perms
    perm = Permission.objects.create(code="folders_can_create")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can create folders")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может создавать папки")

    perm = Permission.objects.create(code="documents_can_create")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can create documents")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может создавать документы")

    # Documents
    perm = Permission.objects.create(code="documents_can_read_last_version")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can read last version of document")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может просматривать последную версию документа")

    perm = Permission.objects.create(code="documents_can_read_previous_versions")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can read document previous versions")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может просматривать предыдущие версии документа")

    perm = Permission.objects.create(code="documents_can_take_document_for_revision")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can take document for revision")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может брать документы на доработку")

    perm = Permission.objects.create(code="documents_can_review")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can review documents")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может обозревать документы")

    perm = Permission.objects.create(code="documents_can_revert")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can revert older version of document")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может вернуть старую версию документа")

    # Activity
    perm = Permission.objects.create(code="activity_can_read")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can read users activity")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может просматривать активность пользователей")

    # Users
    perm = Permission.objects.create(code="users_can_read_profile")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can read users profile")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может просматривать профили пользователей")

    perm = Permission.objects.create(code="users_can_edit")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit users")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать пользователей")

    perm = Permission.objects.create(code="users_can_delete")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can delete users")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может удалять пользователей")

    perm = Permission.objects.create(code="users_can_create")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can create new users")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может создавать новыйх пользователей")

    # Groups
    perm = Permission.objects.create(code="groups_can_create")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can create new groups")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может создавать новые группы")

    perm = Permission.objects.create(code="groups_can_edit")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit groups")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать группы")

    perm = Permission.objects.create(code="groups_can_delete")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can delete groups")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может удалять группы")


def reverse_func(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    PermissionTranslation = apps.get_model("permissions", "PermissionTranslation")

    Permission.objects.get(code="").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('permissions', '0004_auto_20170722_1639'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]