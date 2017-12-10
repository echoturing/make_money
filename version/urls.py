# -*- coding: utf-8 -*-
from django.conf.urls import url

from version.views import need_update

urlpatterns = [
    url(r'^need_update/$', need_update, name="need_update")
]
