# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import json
import random
import uuid

import datetime
import re

import pytz
import requests
from django.conf import settings
from django import forms

PHONE_REG = re.compile("^(13[0-9]|14[579]|15[0-3,5-9]|17[0135678]|18[0-9])\\d{8}$")



def get_rand_int():
    if settings.TEST:
        return "1111"
    return str(random.randrange(1000, 9999))


def get_obj_dict(obj, keys, prefix=''):
    """
    根据对象封装成字典，支持值，函数和有'name'的外键（对象）
    prefix是统一添加的前缀
    """
    record = {}
    for name in keys:
        attr = getattr(obj, name)
        if callable(attr):  # 函数
            record[prefix + name] = attr()
        elif hasattr(attr, "isoformat"):
            record[prefix + name] = attr.isoformat()
        elif hasattr(attr, 'name'):  # 外键
            record[prefix + name] = attr.name
        elif hasattr(attr, 'username'):  # 特殊处理User
            record[prefix + name] = attr.username
        else:
            record[prefix + name] = attr
    return record


class CommonResponse(object):
    def __init__(self, error_code, error_message, data=None):
        self.error_code = error_code
        self.error_message = error_message
        self.data = data

    def to_dict(self):
        return {"error_code": self.error_code,
                "error_message": self.error_message,
                "data": self.data or {}
                }

    def to_json(self):
        return json.dumps(self.to_dict())


class MyMultipleChoiceField(forms.MultipleChoiceField):
    def clean(self, value):
        source_value = super(MyMultipleChoiceField, self).clean(value)
        return json.dumps(source_value)

    def prepare_value(self, value):
        if value is None or value == "":
            return value
        elif isinstance(value, (list, tuple)):
            return value
        return json.loads(value)


def get_current_minute(utc_now):
    """
    :type utc_now datetime.datetime
    """
    total_minutes = utc_now.hour * 60 + utc_now.minute
    return total_minutes


def get_current_second(utc_now):
    total_second = utc_now.hour * 3600 + utc_now.minute * 60 + utc_now.second
    return total_second


def need_push(total_minutes, cycle):
    return not bool(total_minutes % cycle)


def minutes_to_string_tuple(minutes):
    hour = minutes / 60
    minute = minutes % 60
    hour_repr = str(hour) + "小时" if hour else ""
    minute_repr = str(minute) + "分钟" if minute else ""
    return hour_repr, minute_repr


def get_yesterday_range_of_shanghai_tz(utc_datetime):
    """
    获取传入的utc时间的time_zone的昨天的range
    比如  utc时间是2017-12-02 01:00:00+00:00
    返回就是   2017-12-01 09:00:00+08:00
    """
    naive_today = utc_datetime.astimezone(tz=pytz.timezone(settings.TIME_ZONE)).date()
    naive_today = datetime.datetime.combine(naive_today, datetime.time())
    naive_yesterday = naive_today - datetime.timedelta(days=1)
    start_time = naive_yesterday
    start_time_utc = pytz.timezone(settings.TIME_ZONE).localize(start_time, is_dst=None)
    end_time_utc = start_time_utc + datetime.timedelta(days=1)
    return start_time_utc, end_time_utc
