# -*- coding: utf-8 -*-
from django.conf.urls import url

from cash.views import generate_cash_record

urlpatterns = [
    url(r'^generate_cash_record/$', generate_cash_record, name="generate_cash_record"),
]
