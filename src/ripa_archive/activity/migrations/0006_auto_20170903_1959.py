# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-03 19:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20170903_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='document_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='documents.DocumentData'),
        ),
    ]
