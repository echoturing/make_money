# -*- coding: utf-8 -*-
from django.conf.urls import url

from ad.views import *

urlpatterns = [
    url(r'^get_ad_policy/$', get_ad_policy_view, name="get_ad_policy"),
]
