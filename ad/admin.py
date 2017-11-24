# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from account.admin import admin_site
from ad.models import *

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _

from ad.service import get_latest_reward_cycle_count
from money.tool import MyMultipleChoiceField


class AdPolicyAdminForm(forms.ModelForm):
    model = AdPolicy

    def clean(self):
        data = self.cleaned_data
        has_gold = data.get("has_gold")
        if has_gold:
            latest_reward_cycle = get_latest_reward_cycle_count()
            if latest_reward_cycle:
                already_has_gold_count = len(AdPolicy.objects.filter(has_gold=True).exclude(id=self.instance.pk))
                if already_has_gold_count + 1 > latest_reward_cycle.count:
                    raise ValidationError(_('广告位是否有红包设置必须小于等于周期红包个数(当前红包数被设置为{})'.format(latest_reward_cycle.count)),
                                          code='invalid')


class AdPolicyAdmin(admin.ModelAdmin):
    list_display = ["group_id", "ad_position", "edit_by", "last_modify", "has_gold"]
    readonly_fields = ["group_id", "edit_by"]
    form = AdPolicyAdminForm

    def save_model(self, request, obj, form, change):
        if not change:
            raise Exception("不能创建新的对象")
        obj.edit_by = request.user.username
        super(AdPolicyAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


AREA_CHOICE = (("北京市", "北京市"),
               ("天津市", "天津市"),
               ("上海市", "上海市"),
               ("重庆市", "重庆市"),
               ("河北省", "河北省"),
               ("山西省", "山西省"),
               ("辽宁省", "辽宁省"),
               ("吉林省", "吉林省"),
               ("黑龙江省", "黑龙江省"),
               ("江苏省", "江苏省"),
               ("浙江省", "浙江省"),
               ("安徽省", "安徽省"),
               ("福建省", "福建省"),
               ("江西省", "江西省"),
               ("山东省", "山东省"),
               ("河南省", "河南省"),
               ("湖北省", "湖北省"),
               ("湖南省", "湖南省"),
               ("广东省", "广东省"),
               ("海南省", "海南省"),
               ("四川省", "四川省"),
               ("贵州省", "贵州省"),
               ("云南省", "云南省"),
               ("陕西省", "陕西省"),
               ("甘肃省", "甘肃省"),
               ("青海省", "青海省"),
               ("台湾省", "台湾省"),
               ("内蒙古自治区", "内蒙古自治区"),
               ("广西壮族自治区", "广西壮族自治区"),
               ("西藏自治区", "西藏自治区"),
               ("宁夏回族自治区", "宁夏回族自治区"),
               ("新疆维吾尔自治区", "新疆维吾尔自治区"),
               ("香港特别行政区", "香港特别行政区"),
               ("澳门特别行政区", "澳门特别行政区"),
               )


class GlobalShieldConfigAdminForm(forms.ModelForm):
    shield_area = MyMultipleChoiceField(choices=AREA_CHOICE, widget=forms.CheckboxSelectMultiple, label="屏蔽地域")
    model = GlobalShieldConfig


class GlobalShieldConfigAdmin(admin.ModelAdmin):
    list_display = ["shield_type", "comma_split"]

    form = GlobalShieldConfigAdminForm

    def save_model(self, request, obj, form, change):
        if not change:
            raise Exception("不能创建对象")
        if isinstance(obj.shield_area, (list, tuple)):
            obj.shield_area = json.dumps(obj.shield_area)
        elif obj.shield_area == "":
            obj.shield_area = "[]"
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
    readonly_fields = ["first_created", ]

    def save_model(self, request, obj, form, change):
        if change:
            raise Exception("不能修改对象")
        super(ExchangeRateAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


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


admin_site.register(AdPolicy, AdPolicyAdmin)
admin_site.register(RewardCondition, RewardConditionAdmin)
admin_site.register(RewardCycleCount, RewardCycleCountAdmin)
admin_site.register(RewardCycle, RewardCycleAdmin)
admin_site.register(ExchangeRate, ExchangeRateAdmin)
admin_site.register(ChannelShieldConfig, ChannelShieldConfigAdmin)
admin_site.register(GlobalShieldConfig, GlobalShieldConfigAdmin)
admin_site.register(GoldConfig, GoldConfigAdmin)
