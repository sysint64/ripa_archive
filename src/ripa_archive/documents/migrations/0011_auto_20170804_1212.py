# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-04 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20170803_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='remark',
            options={'ordering': ['-datetime']},
        ),
    ]