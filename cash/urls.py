# -*- coding: utf-8 -*-
from django.conf.urls import url

from cash.views import generate_cash_record, get_cash_config_view

urlpatterns = [
    url(r'get_cash_config/$', get_cash_config_view, name="get_cash_config"),
    url(r'^generate_cash_record/$', generate_cash_record, name="generate_cash_record"),
]
