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


class GoldToMoneyRecord(models.Model):
    user = models.OneToOneField(User, verbose_name="用户")
    gold = models.IntegerField(verbose_name="金币", default=0)
    balance = models.IntegerField(verbose_name="人民币(分)", default=0)
    exchange_rate = models.TextField(verbose_name="兑率信息", default="")
    first_created = models.DateTimeField(verbose_name="创建", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)
