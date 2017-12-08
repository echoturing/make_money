# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.html import format_html, format_html_join

from ad.models import ExchangeRate


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="用户")
    gold = models.IntegerField(verbose_name="金币", default=0)
    balance = models.FloatField(verbose_name="余额(分)", default=0)
    cashed_balance = models.FloatField(verbose_name="已提现金额(分)", default=0)
    total_get = models.FloatField(verbose_name="累计收入(分)", default=0)
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    device_token = models.CharField(verbose_name="device_token", max_length=200, default="")
    current_session_id = models.CharField(verbose_name="当前session_id", max_length=100, default="")

    class Meta:
        verbose_name = "用户金币"
        verbose_name_plural = "用户金币"


class GoldToMoneyRecord(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    gold = models.IntegerField(verbose_name="金币", default=0)
    balance = models.IntegerField(verbose_name="人民币(分)", default=0)
    exchange_rate = models.TextField(verbose_name="兑率信息", default="")
    first_created = models.DateTimeField(verbose_name="创建", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "金币转换记录"
        verbose_name_plural = "金币转换记录"


class GetGoldRecord(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    gold = models.IntegerField(verbose_name="获取金币", default=0)
    # ad_source = models.CharField(verbose_name="广告源")
    # ad_type = models.CharField(verbose_name="广告类型")
    # ad_id = models.CharField(verbose_name="广告ID")
    group_id = models.IntegerField(verbose_name="group_id", default=0)
    exchanged = models.BooleanField(verbose_name="是否已转换", default=False)
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "金币获取记录"
        verbose_name_plural = "金币获取记录"
        indexes = [
            models.Index(fields=['user', 'first_created']),
        ]


class UserFeedback(models.Model):
    User = models.ForeignKey(User, verbose_name="用户", default="")
    description = models.TextField(verbose_name="问题描述", default="")
    pictures = models.TextField(verbose_name="图片", default="")
    contact = models.TextField(verbose_name="联系方式", default="")
    phone = models.CharField(verbose_name="手机号", max_length=50, default="")

    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "用户反馈"
        verbose_name_plural = "用户反馈"

    def image_list(self):
        if self.picture_list:
            return format_html_join(format_html('<br/>'), '<a href="{}">{}</a>', ((i, i) for i in self.picture_list))
        return ""

    @property
    def picture_list(self):
        if self.pictures == "":
            return []
        return json.loads(self.pictures)

    image_list.short_description = "图片"
