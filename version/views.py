# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render

# Create your views here.
from version.models import Version


def need_update(request):
    param = json.loads(request.body)
    version = param.get("version")
    # next_version = update_to(version)
    return
