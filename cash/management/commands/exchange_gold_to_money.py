# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from account.models import UserProfile, GoldToMoneyRecord
from ad.service import get_latest_exchange, build_exchange


class Command(BaseCommand):
    help = "把用户的金币兑换成金钱"

    def handle(self, *args, **options):
        user_profile_ids = UserProfile.objects.all().values_list("id")
        for user_profile_id in user_profile_ids:
            user_profile_id = user_profile_id[0]
            with transaction.atomic():
                user_profile = UserProfile.objects.select_for_update().get(id=user_profile_id)
                exchange_rate = get_latest_exchange()
                if user_profile.gold > 0:
                    exchange_dict = build_exchange(exchange_rate)
                    balance = int(1.0 * exchange_rate.money / exchange_rate.gold_count * user_profile.gold)
                    GoldToMoneyRecord.objects.create(user_id=user_profile.user_id, gold=user_profile.gold,
                                                     balance=balance, exchange_rate=json.dumps(exchange_dict))
                    user_profile.balance += balance  # 余额增加
                    user_profile.gold = 0  # 金币置0
                    user_profile.total_get += balance
                    user_profile.save()
