# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 16:23
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    AdPolicy = apps.get_model("ad", "AdPolicy")
    for i in range(30):
        AdPolicy.objects.create(group_id=str(i + 1))


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField(verbose_name='\u7ec4\u53f7')),
                ('ad_position',
                 models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='3',
                                  max_length=20, verbose_name='\u5e7f\u544a\u4f4d\u53f7')),
                ('edit_by', models.CharField(blank=True, max_length=200, verbose_name='\u64cd\u4f5c\u4eba')),
                ('first_created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_modify', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('has_gold', models.BooleanField(default=False, verbose_name='\u6709\u65e0\u91d1\u5e01')),
            ],
        ),
        migrations.RunPython(forwards_func)
    ]
