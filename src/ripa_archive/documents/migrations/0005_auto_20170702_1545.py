# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-02 15:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_auto_20170628_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='folder',
            new_name='parent',
        ),
    ]