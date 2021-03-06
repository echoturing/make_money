# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import F

from statistics.models import Statistics, TStatistics


def statistics_record_event(date, channel, version, ad_source, ad_type, update_key, update_value):
    statistics, _ = Statistics.objects.get_or_create(date=date, channel=channel, version=version,
                                                     ad_source=ad_source, ad_type=ad_type)
    setattr(statistics, update_key, F(update_key) + update_value)
    statistics.save()


def t_statistics_record_event(date, ad_source, ad_position, update_key, update_value):
    t_statistics, _ = TStatistics.objects.get_or_create(date=date, ad_source=ad_source, ad_position=ad_position)
    setattr(t_statistics, update_key, F(update_key) + update_value)
    t_statistics.save()
