# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone

from statistics.service import statistics_record_event


def statistics(request):
    param = json.loads(request.body)
    today = timezone.now()
    channel = param.get("channel")
    version = param.get("version")
    ad_source = param.get("ad_source")
    ad_type = param.get("ad_type")
    update_key = param.get("update_key")
    update_value = param.get("update_value")
    statistics_record_event(today, channel=channel, version=version, ad_source=ad_source, ad_type=ad_type,
                            update_key=update_key, update_value=update_value)
    return HttpResponse("success")
