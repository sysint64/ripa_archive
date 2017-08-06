# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-06 11:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0014_remove_remark_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenteditmeta',
            name='accepted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='remark',
            name='status',
            field=models.CharField(choices=[('0', 'Active'), ('1', 'Accepted'), ('2', 'Rejected'), ('3', 'Finished')], default='0', max_length=1),
        ),
    ]
