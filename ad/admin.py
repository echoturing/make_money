# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin

# Register your models here.
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

from ad.models import AdPolicy, GoldConfig, ExchangeRate, RewardCycle, RewardCycleCount, RewardCondition, \
    GlobalShieldConfig, ChannelShieldConfig


class AdPolicyAdmin(admin.ModelAdmin):
    list_display = ["group_id", "ad_position", "edit_by", "last_modify", "has_gold"]
    readonly_fields = ["group_id", "edit_by"]

    def save_model(self, request, obj, form, change):
        if not change:
            raise Exception("不能创建新的对象")
        obj.edit_by = request.user.username
        super(AdPolicyAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


class GlobalShieldConfigAdmin(admin.ModelAdmin):
    list_display = ["shield_type", "shield_area"]
    readonly_fields = ["shield_type"]

    def save_model(self, request, obj, form, change):
        if not change:
            raise Exception("不能创建对象")
        super(GlobalShieldConfigAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


class ChannelShieldConfigAdminForm(forms.ModelForm):
    def clean(self):
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        if start_time > end_time:
            raise ValidationError(_('开始时间必须小于结束时间'), code='invalid')
        return super(ChannelShieldConfigAdminForm, self).clean()


class ChannelShieldConfigAdmin(admin.ModelAdmin):
    form = ChannelShieldConfigAdminForm
    list_display = ["channel", "start_time", "end_time", "area", "get_status"]


class GoldConfigAdmin(admin.ModelAdmin):
    list_display = ["id", "ad_source", "ad_type", "gold_count"]
    list_display_links = ["id", "ad_source"]
    readonly_fields = ["id", ]


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ["first_created", "gold_count", "money"]


class RewardCycleAdmin(admin.ModelAdmin):
    list_display = ["cycle", "first_created"]

    def save_model(self, request, obj, form, change):
        if change:
            raise Exception("不能修改对象")
        super(RewardCycleAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


class RewardCycleCountAdmin(admin.ModelAdmin):
    list_display = ["count", "first_created"]

    def save_model(self, request, obj, form, change):
        if change:
            raise Exception("不能修改对象")
        super(RewardCycleCountAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


class RewardConditionAdmin(admin.ModelAdmin):
    list_display = ["typ", "first_created"]

    def save_model(self, request, obj, form, change):
        if change:
            raise Exception("不能修改对象")
        super(RewardConditionAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")
