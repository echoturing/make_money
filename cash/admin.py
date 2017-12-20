# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django import forms
from django.contrib import admin

# Register your models here.
from django.db import transaction

from account.admin import admin_site
from account.tasks import push
from cash.models import CashCategory, CashChannel, CashRecord, ACCEPT, REFUSED, CashMoneyCategory
from money.tool import MyMultipleChoiceField
from push.tools import Body, DisplayType, Payload, unicast_push_manager, AfterOpen


class CashChannelAdmin(admin.ModelAdmin):
    list_display = ["name", "first_created", "last_modify"]


CASH_TYPE_CHOICE = (
    (20, 20),
    (30, 30),
    (40, 40),
)


# class CashCategoryAdminForm(forms.ModelForm):
#     money_type = MyMultipleChoiceField(choices=CASH_TYPE_CHOICE, widget=forms.CheckboxSelectMultiple, label="提现金额")
#     model = CashCategory
#

class CashMoneyCategoryAdmin(admin.ModelAdmin):
    pass


admin_site.register(CashMoneyCategory, CashMoneyCategoryAdmin)


class CashCategoryAdmin(admin.ModelAdmin):
    list_display = ["first_created", "channel", "money_type_display", "edit_by", "last_modify"]
    readonly_fields = ["edit_by"]
    filter_horizontal = ("money_type",)


def make_accept(modeladmin, request, queryset):
    for cash_record in queryset:
        with transaction.atomic():
            cash_record.status = ACCEPT
            cash_record.save()
            user_profile = cash_record.user.userprofile
            device_token = user_profile.device_token
            ticker = "您的提现金额{},已打款,您注意查收~".format(cash_record.money / 100.0)
            title = ticker
            text = " "

            builder_id = 2
            body = Body(payload_display_type=DisplayType.notification, after_open=AfterOpen.go_app, ticker=ticker,
                        title=title,
                        text=text, builder_id=builder_id)
            payload = Payload(display_type=DisplayType.notification, body=body)
            push.delay(payload, device_token=device_token)


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
