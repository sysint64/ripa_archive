# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-19 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_activity_document_edit_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='ref_content_type',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='activity',
            name='ref_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='ref_text',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
