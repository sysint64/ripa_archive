# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-05 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_documentcustompermission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentdata',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_data_set', to='documents.Document'),
        ),
    ]
