# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.utils import timezone

from ad.models import AdPolicy, GoldConfig, RewardCycleCount, ExchangeRate, GlobalShieldConfig, ChannelShieldConfig, \
    RewardCycle, RewardCondition, REWARD_CONDITION_CHOICE
from money.tool import get_obj_dict
from push.tools import Filter, Payload, DisplayType, Body, AfterOpen


def build_ad_policy(ad_policy):
    """
    :type ad_policy AdPolicy
    """
    keys = ["group_id", "ad_position", "edit_by", "has_gold", "last_modify"]
    ad_policy_dict = get_obj_dict(ad_policy, keys)
    return ad_policy_dict


def get_ad_policy(**kwargs):
    ad_policies = AdPolicy.objects.filter(**kwargs)
    result = []
    for ad_policy in ad_policies[:30]:
        result.append(build_ad_policy(ad_policy))
    return result


def get_gold_config(**kwargs):
    gold_configs = GoldConfig.objects.all(**kwargs)
    keys = ["id", "ad_source", "ad_type", "gold_count"]
    result = []
    for gold_config in gold_configs:
        result.append(get_obj_dict(gold_config, keys))
    return result


def get_latest_reward_cycle_count():
    """
    :rtype :RewardCycleCount
    """
    latest_reward_cycle = RewardCycleCount.objects.filter().order_by("-first_created").first()
    return latest_reward_cycle


def build_exchange(exchange):
    keys = ["id", "gold_count", "money", "first_created", "last_modify"]
    return get_obj_dict(exchange, keys)


def build_global_shield_config(config):
    keys = ["shield_type", "shield_area"]
    result = get_obj_dict(config, keys)
    result["shield_area"] = json.loads(result["shield_area"])
    return result


def build_channel_shield_config(config):
    keys = ["channel", "start_time", "end_time"]
    return get_obj_dict(config, keys)


def need_shield(channel, city):
    """
    看是否需要屏蔽
    """
    global_shield_config = GlobalShieldConfig.objects.first()
    if city in global_shield_config.area_list:
        return True
    channel_shield_config = ChannelShieldConfig.objects.filter(channel=channel).first()
    return bool(channel_shield_config) and channel_shield_config.need_published()


def get_shield_config():
    """
    获取最新的屏蔽策略
    """
    global_shield_config = GlobalShieldConfig.objects.first()
    global_shield_config_dict = build_global_shield_config(global_shield_config)
    channel_shield_config_list = ChannelShieldConfig.objects.all()
    channel_shield_config_dict_list = []
    for channel_config in channel_shield_config_list:
        channel_shield_config_dict_list.append(build_channel_shield_config(channel_config))
    return global_shield_config_dict, channel_shield_config_dict_list


def build_exchange_rate(exchange):
    keys = ["gold_count", "money", "first_created"]
    return get_obj_dict(exchange, keys)


def get_latest_exchange():
    """
    获取最新的兑换率对象
    :rtype : ExchangeRate
    """
    latest_exchange = ExchangeRate.objects.filter().order_by("-first_created").first()
    return latest_exchange


def get_latest_exchange_rate_json():
    return build_exchange_rate(get_latest_exchange())


def build_reward_cycle(reward_cycle):
    keys = ["cycle", "first_created"]
    return get_obj_dict(reward_cycle, keys)


def get_reward_cycle_json():
    latest_reward_cycle = RewardCycle.objects.filter().order_by("-first_created").first()
    return build_reward_cycle(latest_reward_cycle)


def build_reward_cycle_count(cycle_count):
    keys = ["count", "first_created"]
    return get_obj_dict(cycle_count, keys)


def get_reward_cycle_count_json():
    latest_reward_cycle_count = RewardCycleCount.objects.filter().order_by("-first_created").first()
    return build_reward_cycle_count(latest_reward_cycle_count)


def build_reward_condition(condition):
    keys = ["last", "first_created"]
    return get_obj_dict(condition, keys)


def get_reward_condition_json():
    read_reward_condition = RewardCondition.objects.filter(typ=REWARD_CONDITION_CHOICE[0][0]).order_by(
        "first_created").first()
    download_reward_condition = RewardCondition.objects.filter(typ=REWARD_CONDITION_CHOICE[1][0]).order_by(
        "first_created").first()
    read_reward_condition_json = build_reward_condition(read_reward_condition)
    download_reward_condition_json = build_reward_condition(download_reward_condition)
    return read_reward_condition_json, download_reward_condition_json


def get_current_filter():
    provinces = GlobalShieldConfig.objects.first().area_list

    channels = [build_channel_shield_config(channel_shield_config) for channel_shield_config in
                ChannelShieldConfig.objects.all() if
                channel_shield_config.need_published]
    return Filter(channels=channels, provinces=provinces)
