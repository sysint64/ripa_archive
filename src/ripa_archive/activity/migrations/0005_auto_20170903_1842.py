# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-03 18:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20170819_0741'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(max_length=4)),
                ('ref_text', models.CharField(blank=True, max_length=100)),
                ('details', models.TextField(default='')),
            ],
            options={
                'default_related_name': 'translations',
            },
        ),
        migrations.RemoveField(
            model_name='activity',
            name='details',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='ref_text',
        ),
        migrations.AddField(
            model_name='activitytranslation',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='activity.Activity'),
        ),
    ]