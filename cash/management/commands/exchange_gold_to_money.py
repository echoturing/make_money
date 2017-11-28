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

"""
每天13点执行,把昨天0点到24点获取的金币给转换了
"""


class Command(BaseCommand):
    help = "把用户的金币兑换成金钱"

    def handle(self, *args, **options):
        user_profile_ids = UserProfile.objects.all().values_list("id")
        exchange_rate = get_latest_exchange()
        exchange_dict = build_exchange(exchange_rate)
        yesterday = timezone.now() - datetime.timedelta(days=1)
        start_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(
            hours=8)  # utc时间还得减少8小时
        end_time = start_time + datetime.timedelta(days=1)
        print start_time, end_time
        for user_profile_id in user_profile_ids:
            user_profile_id = user_profile_id[0]
            with transaction.atomic():
                user_profile = UserProfile.objects.select_for_update().get(id=user_profile_id)
                yesterday_user_gold_records = list(GetGoldRecord.objects.filter(user=user_profile.user,
                                                                                first_created__range=(
                                                                                    start_time, end_time)))
                yesterday_user_golds = sum((record.gold for record in yesterday_user_gold_records))

                if yesterday_user_golds > 0:
                    balance = int(1.0 * exchange_rate.money / exchange_rate.gold_count * yesterday_user_golds)

                    GoldToMoneyRecord.objects.create(user_id=user_profile.user_id, gold=yesterday_user_golds,
                                                     balance=balance, exchange_rate=json.dumps(exchange_dict))
                    user_profile.balance += balance  # 余额增加
                    user_profile.gold -= yesterday_user_golds  # 金币减去获取的
                    user_profile.total_get += balance  # 总数增加
                    user_profile.save()
