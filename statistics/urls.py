# -*- coding: utf-8 -*-
from django.conf.urls import url

from statistics.views import statistics, tstatistics

urlpatterns = [
    url(r'^add_record/$', statistics, name="statistics"),
    url(r'^t_add_record/$', tstatistics, name="tstatistics")
]
