# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-06 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0019_auto_20170806_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documenteditmeta',
            name='closed',
        ),
    ]