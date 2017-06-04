# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 12:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('name', models.CharField(max_length=60)),
                ('datetime', models.DateTimeField()),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('allow_delete', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='documentdata',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Folder'),
        ),
        migrations.AddField(
            model_name='documentdata',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Status'),
        ),
    ]
