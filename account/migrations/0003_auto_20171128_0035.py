# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-27 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20171125_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='current_session_id',
            field=models.CharField(default='', max_length=100, verbose_name='\u5f53\u524dsession_id'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='device_token',
            field=models.CharField(default='', max_length=200, verbose_name='device_token'),
        ),
    ]
