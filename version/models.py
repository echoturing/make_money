# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Version(models.Model):
    version_num = models.CharField(verbose_name="版本号", max_length=100, default="", unique=True)

    first_created = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def __unicode__(self):
        return self.version_num

    class Meta:
        verbose_name = "版本配置"
        verbose_name_plural = "版本配置"


class UpdateConfig(models.Model):
    from_version = models.ForeignKey(Version, related_name="update_config_by_from_version", verbose_name="针对版本")
    to_version = models.ForeignKey(Version, related_name="update_config_by_to_version", verbose_name="升级版本")
    edit_by = models.CharField(verbose_name="操作人", max_length=100, default="")
    first_created = models.DateTimeField(verbose_name="创建日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "版本升级控制"
        verbose_name_plural = "版本升级控制"
