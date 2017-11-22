# -*- coding: utf-8 -*-
from ad.models import AdPolicy
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
