# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20171202_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='getgoldrecord',
            name='group_id',
            field=models.IntegerField(default=0, verbose_name='group_id'),
        ),
        migrations.AlterField(
            model_name='getgoldrecord',
            name='first_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='getgoldrecord',
            name='last_modify',
            field=models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4'),
        ),
    ]