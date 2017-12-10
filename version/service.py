# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist

from money.tool import get_obj_dict
from version.models import Version, UpdateConfig


def build_version_update(version, update_config):
    version_keys = ["version_num", "version_name"]
    update_config_keys = ["md5", "url", "release_note", "is_force", "apk_size"]
    result = get_obj_dict(version, version_keys)
    result.update(get_obj_dict(update_config, update_config_keys))
    return result


def update_to(version_num):
    try:
        version = Version.objects.get(version_num=version_num)
    except ObjectDoesNotExist:
        version = None
    if version:
        try:
            update_config = UpdateConfig.objects.get(from_version=version)
        except ObjectDoesNotExist:
            update_config = None
        if update_config:
            return_result = build_version_update(version, update_config)
            return True, return_result
    return False, {}
