# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
from django.utils.html import format_html

AD_POSITION_CHOICE = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


class AdPolicy(models.Model):
    group_id = models.IntegerField(verbose_name="组号")
    ad_position = models.CharField(verbose_name="广告位号", max_length=20, choices=AD_POSITION_CHOICE, default="3"
                                   )
    edit_by = models.CharField(verbose_name="操作人", max_length=200, blank=True)
    has_gold = models.BooleanField(verbose_name="有无金币", default=False)

    first_created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "广告策略设置"
        verbose_name_plural = "广告策略设置"


class GoldConfig(models.Model):
    ad_source = models.CharField(verbose_name="广告源", max_length=200, default="")
    ad_type = models.CharField(verbose_name="广告类型", max_length=50, default="")
    gold_count = models.IntegerField(verbose_name="金币", default=0)

    first_created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "金币设置"
        verbose_name_plural = "金币设置"
        indexes = [
            models.Index(fields=['ad_source', 'ad_type']),
        ]


class GlobalShieldConfig(models.Model):
    shield_type = models.CharField(verbose_name="屏蔽策略", max_length=100, default="")
    shield_area = models.TextField(verbose_name="屏蔽地域", default="")

    first_created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "全局屏蔽设置"
        verbose_name_plural = "全局屏蔽设置"


class ChannelShieldConfig(models.Model):
    channel = models.CharField(verbose_name="渠道屏蔽", max_length=100, default="")
    start_time = models.DateTimeField(verbose_name="开始屏蔽时间")
    end_time = models.DateTimeField(verbose_name="结束屏蔽时间")
    first_created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "渠道屏蔽设置"
        verbose_name_plural = "渠道屏蔽设置"

    def get_status(self):
        now = timezone.now()
        if now < self.start_time:
            return format_html('<span style="color:grey">{}</span>', "待上线")
        elif now > self.end_time:
            return format_html('<span style="color:grey">{}</span>', "已下线")
        return format_html('<span style="color:#32CD32">{}</span>', "已上线")

    get_status.short_description = "状态"

    def area(self):
        area = GlobalShieldConfig.objects.first()
        return area.shield_area

    area.short_description = "屏蔽地域"


class ExchangeRate(models.Model):
    gold_count = models.IntegerField(verbose_name="金币")
    money = models.IntegerField(verbose_name="对应人民币")
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["first_created", ])
        ]
        verbose_name = "金币汇率设置"
        verbose_name_plural = "金币汇率设置"


class RewardCycle(models.Model):
    cycle = models.IntegerField(verbose_name="周期", default=0)
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["first_created", ])
        ]
        verbose_name = "红包周期设置"
        verbose_name_plural = "红包周期设置"


class RewardCycleCount(models.Model):
    count = models.IntegerField(verbose_name="个数", default=0)
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["first_created", ])
        ]
        verbose_name = "红包个数设置"
        verbose_name_plural = "红包个数设置"


REWARD_CONDITION_CHOICE = (
    ('阅读时长', 'read_last'),
    ('下载应用体验时长', 'experience_last'),
)


class RewardCondition(models.Model):
    typ = models.CharField(verbose_name="类型", max_length=50, choices=REWARD_CONDITION_CHOICE)
    last = models.IntegerField(verbose_name="时长", default=10)
    first_created = models.DateTimeField(verbose_name="日期", auto_now_add=True)
    last_modify = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    class Meta:
        verbose_name = "红包领取条件设置"
        verbose_name_plural = "红包领取条件设置"
