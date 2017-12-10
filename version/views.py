# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.views import CONTENT_TYPE_JSON
from money.tool import CommonResponse
from version.service import update_to


def need_update(request):
    param = json.loads(request.body)
    version = param.get("version_num")
    update, return_value = update_to(version)
    return_value["need_update"] = update
    return HttpResponse(CommonResponse(error_code=0, error_message="", data=return_value).to_json(),
                        content_type=CONTENT_TYPE_JSON)
