# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite

from account.models import UserProfile, GoldToMoneyRecord, GetGoldRecord


class MyAdminSite(AdminSite):
    site_title = '后台管理'
    site_header = '后台管理'
    index_title = '后台管理'


admin_site = MyAdminSite(name='manager')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "gold", "balance", "cashed_balance", "total_get", "first_created", "last_modify"]


class GoldToMoneyRecordAdmin(admin.ModelAdmin):
    list_display = ["user", "gold", "balance", "exchange_rate", "first_created", "last_modify"]
    list_filter = ("first_created",)


class GetGoldRecordAdmin(admin.ModelAdmin):
    list_display = ["user", "gold", "exchanged", "first_created"]


admin_site.register(GetGoldRecord, GetGoldRecordAdmin)
admin_site.register(UserProfile, UserProfileAdmin)
admin_site.register(GoldToMoneyRecord, GoldToMoneyRecordAdmin)
