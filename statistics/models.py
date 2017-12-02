# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Statistics(models.Model):
    date = models.DateField(verbose_name="日期")  # 其他地方存utc没问题.这里怕是要存本地时间哦
    channel = models.CharField(verbose_name="渠道", max_length=100, default="")
    version = models.CharField(verbose_name="版本", max_length=40, default="")
    ad_source = models.CharField(verbose_name="广告源", max_length=100, default="")
    ad_type = models.CharField(verbose_name="广告类型", max_length=40, default="")
    show_count = models.IntegerField(verbose_name="展现数", default=0)
    click_count = models.IntegerField(verbose_name="点击数", default=0)
    download_count = models.IntegerField(verbose_name="下载数", default=0)
    success_download_count = models.IntegerField(verbose_name="下载成功数", default=0)
    install_count = models.IntegerField(verbose_name="安装数", default=0)
    success_install_count = models.IntegerField(verbose_name="安装成功数", default=0)
    launch_count = models.IntegerField(verbose_name="打开数", default=0)
    gold_count = models.IntegerField(verbose_name="金币数", default=0)

    first_created = models.DateTimeField(verbose_name="新建时间", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "商业数据系统"
        verbose_name_plural = "商业数据系统"
        unique_together = ("date", "channel", "version", "ad_source", "ad_type")
