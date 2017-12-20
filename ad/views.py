# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection

from account.views import CONTENT_TYPE_JSON
from ad.models import AD_CONFIG_CACHE_KEY, AdConfigCache
from ad.service import get_ad_policy, get_gold_config, get_latest_exchange_rate_json, \
    get_reward_cycle_json, get_reward_cycle_count_json, get_reward_condition_json, need_shield, get_shield_config
from money.tool import CommonResponse

cache = get_redis_connection("default")


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


def need_shield_view(request):
    """
    /ad/need_shield/
    """
    param = json.loads(request.body)
    channel = param.get("channel")
    city = param.get("city")
    need = need_shield(channel, city)
    return HttpResponse(
        CommonResponse(error_code=0, error_message="", data={"need_shield": need}).to_json(),
        content_type=CONTENT_TYPE_JSON
    )


def get_exchange_rate_view(request):
    """
    /ad/get_exchange_rate
    """
    exchange_rate = get_latest_exchange_rate_json()
    return HttpResponse(CommonResponse(error_code=0, error_message="", data={"exchange_rate": exchange_rate}).to_json(),
                        content_type=CONTENT_TYPE_JSON)


def get_reward_cycle_view(request):
    """
    /ad/get_reward_cycle
    """
    get_reward_cycle = get_reward_cycle_json()
    return HttpResponse(
        CommonResponse(error_code=0, error_message="", data={"get_reward_cycle": get_reward_cycle}).to_json(),
        content_type=CONTENT_TYPE_JSON)


def get_reward_cycle_count_view(request):
    """
    /ad/get_reward_cycle_count
    """
    reward_cycle_count = get_reward_cycle_count_json()
    return HttpResponse(
        CommonResponse(error_code=0, error_message="", data={"reward_cycle_count": reward_cycle_count}).to_json(),
        content_type=CONTENT_TYPE_JSON)


def get_reward_condition_view(request):
    """
    /ad/get_reward_condition
    """
    read_reward_condition, download_reward_condition = get_reward_condition_json()
    return HttpResponse(
        CommonResponse(error_code=0, error_message="", data={"read_reward_condition": read_reward_condition,
                                                             "download_reward_condition": download_reward_condition}).to_json(),
        content_type=CONTENT_TYPE_JSON)


def get_ad_config():
    data = AdConfigCache.get_ad_config_cache()
    if data:
        return data
    ad_policies = get_ad_policy()
    gold_configs = get_gold_config()
    read_reward_condition, download_reward_condition = get_reward_condition_json()
    reward_cycle_count = get_reward_cycle_count_json()
    reward_cycle = get_reward_cycle_json()
    data = {
        "ad_policies": ad_policies,  # 红包位置
        "gold_configs": gold_configs,  # 金币设置(广告源,广告类型,金币数)
        "reward_cycle": reward_cycle,  # 红包周期
        "reward_cycle_count": reward_cycle_count,  # 周期红包数
        "read_reward_condition": read_reward_condition,  # 阅读红包领取条件
        "download_reward_condition": download_reward_condition,  # 下载红包领取条件

    }
    AdConfigCache.set_ad_config_cache(data)
    return data


def get_ad_config_view(request):
    """
    /ad/get_ad_config
    """
    data = get_ad_config()
    return HttpResponse(
        CommonResponse(error_code=0, error_message="", data=data).to_json(),
        content_type=CONTENT_TYPE_JSON)
