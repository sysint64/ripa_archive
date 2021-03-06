# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-11 16:40
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    PermissionTranslation = apps.get_model("permissions", "PermissionTranslation")

    # Folders
    perm = Permission.objects.create(code="folders_can_edit")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit folder")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать дирректорию")

    perm = Permission.objects.create(code="folders_can_edit_permissions")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit folder permissions")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать права на дирректори")

    perm = Permission.objects.create(code="folders_can_delete")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can delete folder")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может удалить дирректорию")

    # Permissions inside folder
    perm = Permission.objects.create(code="folders_can_read")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can read folder")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может просматривать содержимое дирректории")

    perm = Permission.objects.create(code="folders_can_edit_folders_inside_this_folder")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit folders inside this folder")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать дирректории, находящиеся внутри этой дирректории")

    perm = Permission.objects.create(code="folders_can_delete_folders_inside_this_folder")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can delete folders inside this folder")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может удалять дирректории, находящиеся внутри этой дирректории")

    perm = Permission.objects.create(code="folders_can_create_folders_inside_this_folder")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can create folders")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может создавать новые дирректории")

    perm = Permission.objects.create(code="folders_can_edit_permissions_to_exist")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit permissions to exist folders")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать права на дирректории внутри этой дирректории")

    perm = Permission.objects.create(code="folders_can_edit_permissions_to_own")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit permissions to own folders")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать права на свои дирректории (созданные этим пользователем)")

    # Permissions on documents inside folders
    perm = Permission.objects.create(code="folders_can_edit_documents_inside_this_folder")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit documents inside this folder")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать документы, находящиеся внутри этой дирректории")

    perm = Permission.objects.create(code="folders_can_delete_documents_inside_this_folder")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can delete documents inside this folder")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может удалять дирректории, находящиеся внутри этой дирректории")

    perm = Permission.objects.create(code="folders_can_create_documents_inside_this_folder")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can create documents")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может создавать новые документы")

    perm = Permission.objects.create(code="folders_can_set_custom_permissions_to_exist_documents")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can set custom permissions to exist documents")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может назначать права на существующие документы")

    perm = Permission.objects.create(code="folders_can_set_custom_permissions_to_own_documents")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can set custom permissions to own documents")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может назначать права на свои документы (созданные этим пользователем)")

    # Documents
    perm = Permission.objects.create(code="documents_can_read")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can read document")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может читать документ")

    perm = Permission.objects.create(code="documents_can_edit")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit document")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать документ")

    perm = Permission.objects.create(code="documents_can_delete")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can delete document")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может удалить документ")

    perm = Permission.objects.create(code="documents_can_edit_permissions")
    PermissionTranslation.objects.create(permission=perm, language_code="en", name="Can edit document permissions")
    PermissionTranslation.objects.create(permission=perm, language_code="ru", name="Может редактировать права на документ")


def reverse_func(apps, schema_editor):
    Permission = apps.get_model("permissions", "Permission")
    PermissionTranslation = apps.get_model("permissions", "PermissionTranslation")

    Permission.objects.all().delete()
    PermissionTranslation.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
