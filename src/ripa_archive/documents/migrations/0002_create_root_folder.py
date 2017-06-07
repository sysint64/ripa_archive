# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards_func(apps, schema_editor):
    Folder = apps.get_model("documents", "Folder")
    Folder.objects.create(name="Root", parent=None)


def reverse_func(apps, schema_editor):
    Folder = apps.get_model("documents", "Folder")
    Folder.objects.filter(name="Root", parent=None)


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
