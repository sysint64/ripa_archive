# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-03 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170827_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Avatar image'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('0', 'Unset'), ('m', 'Male'), ('f', 'Female')], default='0', max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Is active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=255, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=100, verbose_name='Position'),
        ),
        migrations.AlterField(
            model_name='user',
            name='web_site',
            field=models.URLField(blank=True, max_length=100, verbose_name='Web site'),
        ),
    ]
