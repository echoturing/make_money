# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Statistics(models.Model):
    date = models.DateField(verbose_name="日期")
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
        verbose_name = "商业数据系统1"
        verbose_name_plural = "商业数据系统1"
        unique_together = ("date", "channel", "version", "ad_source", "ad_type")


class TStatistics(models.Model):
    date = models.DateField(verbose_name="日期")
    ad_source = models.CharField(verbose_name="广告源", max_length=100, default="")
    ad_position = models.CharField(verbose_name="广告位", max_length=100, default="")
    request_time = models.IntegerField(verbose_name="请求次数", default=0)
    request_count = models.IntegerField(verbose_name="请求条数", default=0)
    return_count = models.IntegerField(verbose_name="返回广告数", default=0)
    show_count = models.IntegerField(verbose_name="展现数", default=0)

    class Meta:
        verbose_name = "商业数据系统2"
        verbose_name_plural = "商业数据系统2"
        unique_together = ("date", "ad_source", "ad_position")

    def fill_percent(self):
        if self.request_count == 0:
            return 0
        return 1.0 * self.return_count / self.request_count

    fill_percent.short_description = "填充率"

    def show_percent(self):
        if self.return_count == 0:
            return 0
        return 1.0 * self.show_count / self.return_count

    show_percent.short_description = "展现率"
