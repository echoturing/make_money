# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite

from ad.admin import *


class MyAdminSite(AdminSite):
    site_title = '后台管理'
    site_header = '后台管理'
    index_title = '后台管理'


admin_site = MyAdminSite(name='administrator')
admin_site.register(AdPolicy, AdPolicyAdmin)
# admin_site.register(RewardCondition, RewardConditionAdmin)
# admin_site.register(RewardCycleCount, RewardCycleCountAdmin)
# admin_site.register(RewardCycle, RewardCycleAdmin)
# admin_site.register(ExchangeRate, ExchangeRateAdmin)
# admin_site.register(ChannelShieldConfig, ChannelShieldConfigAdmin)
# admin_site.register(GlobalShieldConfig, GlobalShieldConfigAdmin)
admin_site.register(GoldConfig, GoldConfigAdmin)
