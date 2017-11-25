# -*- coding: utf-8 -*-
from django.conf.urls import url

from ad.views import *

urlpatterns = [
    url(r'^get_ad_policy/$', get_ad_policy_view, name="get_ad_policy"),
    url(r'^get_gold_config/$', get_gold_config_view, name="get_gold_config"),
    url(r'^get_shield_config/$', get_shield_config_view, name="get_shield_config"),
]
