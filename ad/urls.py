# -*- coding: utf-8 -*-
from django.conf.urls import url

from ad.views import *

urlpatterns = [
    url(r'^get_ad_policy/$', get_ad_policy_view, name="get_ad_policy"),
    url(r'^get_gold_config/$', get_gold_config_view, name="get_gold_config"),
    url(r'^get_shield_config/$', get_shield_config_view, name="get_shield_config"),
    url(r'^need_shield/$', need_shield_view, name="need_shield"),
    url(r'^get_exchange_rate/$', get_exchange_rate_view, name="get_exchange_rate"),
    url(r'^get_reward_cycle/$', get_reward_cycle_view, name="get_reward_cycle"),
    url(r'^get_reward_cycle_count/$', get_reward_cycle_count_view, name="get_reward_cycle_count"),
    url(r'^get_reward_condition/$', get_reward_condition_view, name="get_reward_condition"),

    url(r'^get_ad_config/$', get_ad_config_view, name="get_ad_config_view")
]
