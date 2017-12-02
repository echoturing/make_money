# -*- coding: utf-8 -*-
from django.conf.urls import url

from statistics.views import statistics

urlpatterns = [
    url(r'^add_record/$', statistics, name="statistics")
]
