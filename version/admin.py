# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from account.admin import admin_site
from version.models import Version, UpdateConfig


class VersionAdmin(admin.ModelAdmin):
    list_display = ["version_num", "first_created", "last_modify"]


class UpdateConfigAdmin(admin.ModelAdmin):
    list_display = ["from_version", "to_version", "edit_by", "first_created", "last_modify"]
    readonly_fields = ["edit_by",]

    def save_model(self, request, obj, form, change):
        obj.edit_by = request.user.username
        super(UpdateConfigAdmin, self).save_model(request, obj, form, change)


admin_site.register(Version, VersionAdmin)
admin_site.register(UpdateConfig, UpdateConfigAdmin)
