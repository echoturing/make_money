# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import pytz
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from pytz import UTC

from money.tool import get_yesterday_range_of_shanghai_tz
from statistics.service import *


# Create your tests here.


class FuckTestCase(TestCase):
    def setUp(self):
        pass

    def test_record_event(self):
        date = timezone.now()
        channel = "应用宝"
        version = "1.1.1"
        ad_source = "广点通"
        ad_type = "阅读广告"
        update_key = "install_count"

        update_value = 2
        statistics_record_event(date=date, channel=channel, version=version, ad_source=ad_source, ad_type=ad_type,
                                update_key=update_key, update_value=update_value)
        statistics_record_event(date=date, channel=channel, version=version, ad_source=ad_source, ad_type=ad_type,
                                update_key=update_key, update_value=update_value)

        statistics = Statistics.objects.get(date=date, channel=channel, version=version, ad_source=ad_source,
                                            ad_type=ad_type,
                                            )
        self.assertEqual(statistics.install_count, 4)

    def test_get_yesterday_range_of_shanghai_tz(self):
        now = datetime.datetime(2017, 12, 02, 16, 1, 1).replace(tzinfo=UTC)
        start_time, end_time = get_yesterday_range_of_shanghai_tz(now)
        self.assertEqual(start_time,
                         (datetime.datetime(2017, 12, 02) - datetime.timedelta(hours=8)).replace(tzinfo=UTC))
        now = datetime.datetime(2017, 12, 02, 15, 1, 1).replace(tzinfo=UTC)
        start_time, end_time = get_yesterday_range_of_shanghai_tz(now)
        self.assertEqual(start_time,
                         (datetime.datetime(2017, 12, 01) - datetime.timedelta(hours=8)).replace(tzinfo=UTC))
