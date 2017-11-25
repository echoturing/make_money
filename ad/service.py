# -*- coding: utf-8 -*-
from ad.models import AdPolicy, GoldConfig, RewardCycleCount, ExchangeRate
from money.tool import get_obj_dict


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


def get_latest_exchange():
    """
    获取最新的兑换率对象
    :rtype : ExchangeRate
    """
    latest_exchange = ExchangeRate.objects.filter().order_by("-first_created").first()
    return latest_exchange
