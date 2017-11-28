# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-28 14:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20171128_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getgoldrecord',
            name='first_created',
            field=models.DateTimeField(verbose_name='\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='getgoldrecord',
            name='last_modify',
            field=models.DateTimeField(verbose_name='\u4fee\u6539\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='getgoldrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
    ]