# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.admin import AdminSite

from account.models import UserProfile, GoldToMoneyRecord


class MyAdminSite(AdminSite):
    site_title = '后台管理'
    site_header = '后台管理'
    index_title = '后台管理'


admin_site = MyAdminSite(name='manager')

# admin_site.register(UserProfile)
# admin_site.register(GoldToMoneyRecord)
