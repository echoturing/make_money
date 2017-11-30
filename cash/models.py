# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CashChannel(models.Model):
    name = models.CharField(verbose_name="提现渠道名字", max_length=100)
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "提现渠道类设别置"
        verbose_name_plural = "提现渠道类设别置"


class CashCategory(models.Model):
    channel = models.ForeignKey(CashChannel, verbose_name="提现方式")

    money_type = models.TextField(verbose_name="提现金额(分)", default="")
    edit_by = models.CharField(verbose_name="操作人", max_length=100, default="")
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def __unicode__(self):
        return self.channel.name

    def money_type_comma(self):
        return ",".join(json.loads(self.money_type))

    money_type_comma.short_description = "提现金额(分)"

    class Meta:
        verbose_name = "提现金额设置"
        verbose_name_plural = "提现金额设置"


CASH_RECORD_STATUS = (
    ("待审核", "待审核"),
    ("已通过", "已通过"),
    ("已拒绝", "已拒绝"),
)
ACCEPT = CASH_RECORD_STATUS[1][1]
REFUSED = CASH_RECORD_STATUS[2][1]


class CashRecord(models.Model):
    channel = models.CharField(verbose_name="渠道", max_length=50, default="")
    device_brand = models.CharField(verbose_name="手机品牌", max_length=50, default="")
    version_num = models.CharField(verbose_name="版本", max_length=50, default="")

    user = models.ForeignKey(User, verbose_name="用户手机号", to_field="username")
    phone = models.CharField(verbose_name="用户填写的手机号", max_length=30)

    device_id = models.CharField(verbose_name="device_id", max_length=200, default="")

    real_name = models.CharField(verbose_name="姓名", max_length=50)
    identity = models.CharField(verbose_name="身份证号", max_length=100)
    machine_type = models.CharField(verbose_name="机型", max_length=100)

    cash_type = models.CharField(verbose_name="微信号/支付宝", max_length=100, default="")
    money = models.IntegerField(verbose_name="提现金额(分)", default=0)
    status = models.CharField(verbose_name="状态", max_length=30, choices=CASH_RECORD_STATUS)
    reason = models.CharField(verbose_name="原因", max_length=200, default="", blank=True)

    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "提现记录"
        verbose_name_plural = "提现记录"
