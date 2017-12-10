# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from account.admin import admin_site
from statistics.models import Statistics, TStatistics


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ["date", "channel", "version", "ad_source", "ad_type", "show_count", "click_count", "download_count",
                    "success_download_count", "install_count", "success_install_count", "launch_count", "gold_count"]

    def get_actions(self, request):
        actions = super(StatisticsAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


class TStatisticsAdmin(admin.ModelAdmin):
    list_display = ["date", "ad_source", "ad_position", "request_time", "request_count", "return_count", "show_count",
                    "fill_percent", "show_percent"]

    def get_actions(self, request):
        actions = super(TStatisticsAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


admin_site.register(Statistics, StatisticsAdmin)
admin_site.register(TStatistics, TStatisticsAdmin)
