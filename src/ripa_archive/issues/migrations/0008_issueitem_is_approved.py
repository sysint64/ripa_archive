# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-19 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0007_issueitem_is_paused'),
    ]

    operations = [
        migrations.AddField(
            model_name='issueitem',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
