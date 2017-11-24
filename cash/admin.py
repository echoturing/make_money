# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from django.contrib import admin

# Register your models here.
from account.admin import admin_site
from cash.models import CashCategory, CashChannel
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


admin_site.register(CashCategory, CashCategoryAdmin)
admin_site.register(CashChannel, CashChannelAdmin)
