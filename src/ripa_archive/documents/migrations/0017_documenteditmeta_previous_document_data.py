# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-06 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0016_document_accepted_edit_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenteditmeta',
            name='previous_document_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='documents.DocumentData'),
        ),
    ]
