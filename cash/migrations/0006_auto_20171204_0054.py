# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0005_auto_20171203_1601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cashchannel',
            options={'verbose_name': '\u63d0\u73b0\u6e20\u9053\u7c7b\u522b\u8bbe\u7f6e', 'verbose_name_plural': '\u63d0\u73b0\u6e20\u9053\u7c7b\u522b\u8bbe\u7f6e'},
        ),
        migrations.AlterModelOptions(
            name='cashmoneycategory',
            options={'verbose_name': '\u63d0\u73b0\u91d1\u989d\u7c7b\u522b\u8bbe\u7f6e', 'verbose_name_plural': '\u63d0\u73b0\u91d1\u989d\u7c7b\u522b\u8bbe\u7f6e'},
        ),
        migrations.AlterModelOptions(
            name='cashrecord',
            options={'verbose_name': '\u63d0\u73b0\u5ba1\u6838\u540e\u53f0', 'verbose_name_plural': '\u63d0\u73b0\u5ba1\u6838\u540e\u53f0'},
        ),
    ]