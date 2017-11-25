# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.views import CONTENT_TYPE_JSON
from ad.service import get_ad_policy, get_gold_config, get_shield_config
from money.tool import CommonResponse


# @login_required
def get_ad_policy_view(request):
    """
    /ad/get_ad_policy
    """
    ad_policies = get_ad_policy()
    return HttpResponse(CommonResponse(error_code=0, error_message="", data={"ad_policies": ad_policies}).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def get_gold_config_view(request):
    """
    /ad/get_gold_config
    """
    gold_configs = get_gold_config()
    return HttpResponse(CommonResponse(error_code=0, error_message="", data={"gold_configs": gold_configs}).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def get_shield_config_view(request):
    """
    /ad/get_shield_config
    """
    global_shield_config, channel_shield_config_list = get_shield_config()
    return HttpResponse(
        CommonResponse(error_code=0, error_message="", data={"global_shield_config": global_shield_config,
                                                             "channel_shield_config_list": channel_shield_config_list,
                                                             }).to_json(),
        content_type=CONTENT_TYPE_JSON
    )
