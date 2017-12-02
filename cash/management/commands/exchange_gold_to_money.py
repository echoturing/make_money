# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from pytz import utc

from account.models import UserProfile, GoldToMoneyRecord, GetGoldRecord
from ad.service import get_latest_exchange, build_exchange
from django.utils import timezone

from money.tool import get_yesterday_range_of_shanghai_tz
from push.tools import Body, DisplayType, AfterOpen, Payload, unicast_push_manager

"""
每天13点执行,把昨天0点到24点获取的金币给转换了
"""


class Command(BaseCommand):
    help = "把用户的金币兑换成金钱"

    def handle(self, *args, **options):
        user_profile_ids = UserProfile.objects.all().values_list("id")
        exchange_rate = get_latest_exchange()
        exchange_dict = build_exchange(exchange_rate)
        start_time, end_time = get_yesterday_range_of_shanghai_tz(timezone.now())
        for user_profile_id in user_profile_ids:
            user_profile_id = user_profile_id[0]
            with transaction.atomic():
                user_profile = UserProfile.objects.select_for_update().get(id=user_profile_id)
                yesterday_user_gold_records = GetGoldRecord.objects.filter(user=user_profile.user,
                                                                           first_created__range=(
                                                                               start_time, end_time),
                                                                           exchanged=False)  # 未兑换的

                yesterday_user_golds = sum((record.gold for record in yesterday_user_gold_records))

                if yesterday_user_golds > 0:
                    balance = int(1.0 * exchange_rate.money / exchange_rate.gold_count * yesterday_user_golds)

                    GoldToMoneyRecord.objects.create(user_id=user_profile.user_id, gold=yesterday_user_golds,
                                                     balance=balance, exchange_rate=json.dumps(exchange_dict))
                    user_profile.balance += balance  # 余额增加
                    user_profile.gold -= yesterday_user_golds  # 金币减去获取的
                    user_profile.total_get += balance  # 总数增加
                    user_profile.save()
                    self.push_to_user(user_profile)
                    yesterday_user_gold_records.update(exchanged=True)

    @staticmethod
    def push_to_user(user_profile):
        device_token = user_profile.device_token
        ticker = "您昨天获得的金币已折算成现金,今天继续赚钱哦~"
        title = ticker
        text = " "
        builder_id = 3
        body = Body(payload_display_type=DisplayType.notification, after_open=AfterOpen.go_app, ticker=ticker,
                    title=title,
                    text=text, builder_id=builder_id)

        payload = Payload(display_type=DisplayType.notification, body=body)
        unicast_push_manager.push(payload, device_token=device_token)
