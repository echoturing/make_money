# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

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

    money_type = models.TextField(verbose_name="提现金额", default="")
    edit_by = models.CharField(verbose_name="操作人", max_length=100, default="")
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def __unicode__(self):
        return self.channel.name

    def money_type_comma(self):
        return ",".join(json.loads(self.money_type))

    class Meta:
        verbose_name = "提现金额设置"
        verbose_name_plural = "提现金额设置"
