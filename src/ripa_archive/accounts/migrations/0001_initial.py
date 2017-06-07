# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('0', 'Незадан'), ('m', 'Мужской'), ('f', 'Женский')], default='0', max_length=1, verbose_name='gender')),
                ('avatar_image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to='')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
