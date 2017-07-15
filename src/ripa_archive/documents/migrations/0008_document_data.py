# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-11 16:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20170705_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='data',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='documents.DocumentData'),
        ),
    ]