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


class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        AdConfigCache.expire_ad_config_cache()
        return super(BaseAdmin, self).save_model(request, obj, form, change)


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


class AdPolicyAdmin(BaseAdmin):
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


AREA_CHOICE = (
    ("北京", "北京",),
    ("上海", "上海",),
    ("广东", "广东",),
    ("安徽", "安徽",),
    ("澳门", "澳门",),
    ("重庆", "重庆",),
    ("福建", "福建",),
    ("甘肃", "甘肃",),
    ("广西", "广西",),
    ("贵州", "贵州",),
    ("海南", "海南",),
    ("河北", "河北",),
    ("河南", "河南",),
    ("黑龙江", "黑龙江"),
    ("湖北", "湖北",),
    ("湖南", "湖南",),
    ("吉林", "吉林",),
    ("江苏", "江苏",),
    ("江西", "江西",),
    ("辽宁", "辽宁",),
    ("内蒙", "内蒙",),
    ("宁夏", "宁夏",),
    ("青海", "青海",),
    ("山东", "山东",),
    ("山西", "山西",),
    ("陕西", "陕西",),
    ("四川", "四川",),
    ("天津", "天津",),
    ("西藏", "西藏",),
    ("香港", "香港",),
    ("新疆", "新疆",),
    ("云南", "云南",),
    ("浙江", "浙江",),

)


class GlobalShieldConfigAdminForm(forms.ModelForm):
    shield_area = MyMultipleChoiceField(choices=AREA_CHOICE, widget=forms.CheckboxSelectMultiple, label="屏蔽地域")
    model = GlobalShieldConfig


class GlobalShieldConfigAdmin(BaseAdmin):
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


class ChannelShieldConfigAdmin(BaseAdmin):
    form = ChannelShieldConfigAdminForm
    list_display = ["channel", "start_time", "end_time", "area", "get_status"]


class GoldConfigAdmin(BaseAdmin):
    list_display = ["id", "ad_source", "ad_type", "gold_count"]
    list_display_links = ["id", "ad_source"]
    readonly_fields = ["id", ]


class ExchangeRateAdmin(BaseAdmin):
    list_display = ["first_created", "gold_count", "money"]
    readonly_fields = ["first_created", ]

    def save_model(self, request, obj, form, change):
        if change:
            raise Exception("不能修改对象")
        super(ExchangeRateAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


class RewardCycleAdmin(BaseAdmin):
    list_display = ["cycle", "first_created"]

    def save_model(self, request, obj, form, change):
        if change:
            raise Exception("不能修改对象")
        super(RewardCycleAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


class RewardCycleCountAdmin(BaseAdmin):
    list_display = ["count", "first_created"]

    def save_model(self, request, obj, form, change):
        if change:
            raise Exception("不能修改对象")
        super(RewardCycleCountAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")


class RewardConditionAdmin(BaseAdmin):
    list_display = ["typ", "first_created"]


admin_site.register(AdPolicy, AdPolicyAdmin)
admin_site.register(RewardCondition, RewardConditionAdmin)
admin_site.register(RewardCycleCount, RewardCycleCountAdmin)
admin_site.register(RewardCycle, RewardCycleAdmin)
admin_site.register(ExchangeRate, ExchangeRateAdmin)
admin_site.register(ChannelShieldConfig, ChannelShieldConfigAdmin)
admin_site.register(GlobalShieldConfig, GlobalShieldConfigAdmin)
admin_site.register(GoldConfig, GoldConfigAdmin)
