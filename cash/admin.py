# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from django.contrib import admin

# Register your models here.
from account.admin import admin_site
from cash.models import CashCategory, CashChannel, CashRecord, ACCEPT, REFUSED
from money.tool import MyMultipleChoiceField


class CashChannelAdmin(admin.ModelAdmin):
    list_display = ["name", "first_created", "last_modify"]


CASH_TYPE_CHOICE = (
    (20, 20),
    (30, 30),
    (40, 40),
)


class CashCategoryAdminForm(forms.ModelForm):
    money_type = MyMultipleChoiceField(choices=CASH_TYPE_CHOICE, widget=forms.CheckboxSelectMultiple, label="提现金额")
    model = CashCategory


class CashCategoryAdmin(admin.ModelAdmin):
    list_display = ["first_created", "channel", "money_type_comma", "edit_by", "last_modify"]
    readonly_fields = ["edit_by"]
    form = CashCategoryAdminForm

    def save_model(self, request, obj, form, change):
        obj.edit_by = request.user.username
        if isinstance(obj.money_type, (list, tuple)):
            obj.money_type = json.dumps(obj.money_type)
        elif obj.money_type == "":
            obj.money_type = "[]"
        super(CashCategoryAdmin, self).save_model(request, obj, form, change)


def make_accept(modeladmin, request, queryset):
    queryset.update(status=ACCEPT)


make_accept.short_description = "全部通过"


def make_refused(modeladmin, request, queryset):
    queryset.update(status=REFUSED)


make_refused.short_description = "全部拒绝"


class CashRecordAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "phone", "device_id", "real_name", "identity", "machine_type", "cash_type", "money",
                    "status", "reason"]

    list_filter = ["cash_type", ]

    def save_model(self, request, obj, form, change):
        if not change:
            raise Exception("不能创建对象")
        super(CashRecordAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        raise Exception("不能删除对象")

    def add_view(self, request, form_url='', extra_context=None):
        raise Exception("不能创建对象")

    actions = [make_accept, make_refused]

    def get_actions(self, request):
        actions = super(CashRecordAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


admin_site.register(CashRecord, CashRecordAdmin)
admin_site.register(CashCategory, CashCategoryAdmin)
admin_site.register(CashChannel, CashChannelAdmin)
