# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction

from account.models import UserProfile
from cash.models import CashRecord


def generate_cash_record(user, money, phone, real_name, device_id, identity, machine_type, cash_type, device_brand,
                         channel, version_num):
    with transaction.atomic():
        user_profile = UserProfile.objects.select_for_update().get(user_id=user.id)
        if money > user_profile.balance:
            return 401, "提现金额大于已有金额"
        user_profile.balance -= money
        user_profile.cashed_balance += money
        user_profile.save()
        CashRecord.objects.create(user=user, money=money, phone=phone, real_name=real_name, device_brand=device_brand,
                                  device_id=device_id,
                                  identity=identity, machine_type=machine_type, cash_type=cash_type, channel=channel,
                                  version_num=version_num,
                                  )
        return 0, "提现记录生成成功"
