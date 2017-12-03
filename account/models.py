# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from ad.models import ExchangeRate


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="用户")
    gold = models.IntegerField(verbose_name="金币", default=0)
    balance = models.IntegerField(verbose_name="余额(分)", default=0)
    cashed_balance = models.IntegerField(verbose_name="已提现金额(分)", default=0)
    total_get = models.IntegerField(verbose_name="累计收入(分)", default=0)
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
    exchanged = models.BooleanField(verbose_name="是否已转换", default=False)
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "金币获取记录"
        verbose_name_plural = "金币获取记录"
        indexes = [
            models.Index(fields=['user', 'first_created']),
        ]
