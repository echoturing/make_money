# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0002_auto_20171121_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerate',
            name='money',
            field=models.IntegerField(verbose_name='\u5bf9\u5e94\u4eba\u6c11\u5e01(\u5206)'),
        ),
        migrations.AlterField(
            model_name='rewardcondition',
            name='typ',
            field=models.CharField(choices=[('read_last', '\u9605\u8bfb\u65f6\u957f'), ('experience_last', '\u4e0b\u8f7d\u5e94\u7528\u4f53\u9a8c\u65f6\u957f')], max_length=50, verbose_name='\u7c7b\u578b'),
        ),
    ]
